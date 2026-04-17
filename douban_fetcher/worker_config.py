"""
多设备配置模块
"""
import socket
import uuid


def get_worker_id() -> str:
    """
    生成唯一的设备标识
    
    Returns:
        设备标识字符串
    """
    # 方式1：使用主机名 + UUID（推荐）
    hostname = socket.gethostname()
    unique_id = str(uuid.uuid4())[:8]
    return f"{hostname}_{unique_id}"


def get_simple_worker_id() -> str:
    """
    生成简单的设备标识（仅使用主机名）
    
    Returns:
        设备标识字符串
    """
    return socket.gethostname()
