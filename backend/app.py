import os
import platform
import socket
import time
from datetime import datetime, timezone

import docker
import psutil
from flask import Flask, jsonify

app = Flask(__name__)


@app.get('/api/health')
def health_check():
    """Simple endpoint to verify backend is running and env vars are loaded."""
    return jsonify({
        "status": "ok",
        "service": "backend",
        "database": {
            "host": os.getenv("DB_HOST", "not-set"),
            "port": os.getenv("DB_PORT", "not-set"),
            "name": os.getenv("DB_NAME", "not-set"),
            "user": os.getenv("DB_USER", "not-set"),
        },
    })


def get_docker_client():
    """Create a Docker client if Docker socket is available."""
    try:
        return docker.from_env()
    except Exception:
        return None


def get_containers_data():
    """Return all container states from the local Docker daemon."""
    client = get_docker_client()
    if client is None:
        return {
            "docker_access": "unavailable",
            "error": "Docker socket not accessible from backend container.",
            "containers": [],
        }

    try:
        containers = client.containers.list(all=True)
        result = []
        for c in containers:
            result.append({
                "id": c.short_id,
                "name": c.name,
                "image": c.image.tags[0] if c.image.tags else c.image.short_id,
                "state": c.attrs.get("State", {}).get("Status", "unknown"),
                "status": c.status,
            })

        return {
            "docker_access": "ok",
            "count": len(result),
            "containers": sorted(result, key=lambda item: item["name"]),
        }
    except Exception as exc:
        return {
            "docker_access": "error",
            "error": str(exc),
            "containers": [],
        }


def get_system_data():
    """Return machine and runtime information for learning/visibility."""
    vm = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=0.2)

    data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        },
        "cpu": {
            "logical_cores": psutil.cpu_count(logical=True),
            "usage_percent": cpu_percent,
            "load_avg_1m_5m_15m": (
                list(os.getloadavg()) if hasattr(os, "getloadavg") else None
            ),
        },
        "memory": {
            "total_mb": round(vm.total / (1024 * 1024), 2),
            "available_mb": round(vm.available / (1024 * 1024), 2),
            "used_percent": vm.percent,
        },
        "uptime": {
            "seconds": round(time.time() - psutil.boot_time(), 2),
            "boot_time_utc": datetime.fromtimestamp(
                psutil.boot_time(), timezone.utc
            ).isoformat(),
        },
    }

    client = get_docker_client()
    if client is not None:
        try:
            info = client.info()
            data["docker_host"] = {
                "name": info.get("Name"),
                "server_version": client.version().get("Version"),
                "operating_system": info.get("OperatingSystem"),
                "kernel_version": info.get("KernelVersion"),
                "cpus": info.get("NCPU"),
                "total_memory_mb": round(info.get("MemTotal", 0) / (1024 * 1024), 2),
            }
        except Exception as exc:
            data["docker_host"] = {"error": str(exc)}
    else:
        data["docker_host"] = {"error": "Docker socket not accessible."}

    return data


@app.get('/api/containers')
def containers():
    return jsonify(get_containers_data())


@app.get('/api/system')
def system():
    return jsonify(get_system_data())


@app.get('/api/dashboard')
def dashboard():
    """Combined endpoint for frontend dashboard refresh."""
    return jsonify({
        "health": health_check().get_json(),
        "containers": get_containers_data(),
        "system": get_system_data(),
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
