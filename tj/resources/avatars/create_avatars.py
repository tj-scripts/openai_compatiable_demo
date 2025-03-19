"""
Create avatar images for the chat interface.

Author: tj-scripts
Email: tangj1984@gmail.com
Date: 2024-03-21
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_user_avatar(size: int = 128) -> Image.Image:
    """Create a user avatar image.
    
    Args:
        size: Image size in pixels
        
    Returns:
        PIL Image object
    """
    # 创建新图片
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    draw.ellipse([0, 0, size-1, size-1], fill=(66, 133, 244, 255))
    
    # 绘制用户图标
    center = size // 2
    radius = size // 4
    
    # 头部
    head_radius = radius * 1.2
    draw.ellipse([
        center - head_radius,
        center - head_radius * 1.5,
        center + head_radius,
        center + head_radius * 0.5
    ], fill=(255, 255, 255, 255))
    
    # 身体
    body_width = radius * 1.5
    body_height = radius * 2
    draw.rectangle([
        center - body_width // 2,
        center + head_radius * 0.5,
        center + body_width // 2,
        center + head_radius * 0.5 + body_height
    ], fill=(255, 255, 255, 255))
    
    # 添加阴影效果
    shadow_color = (0, 0, 0, 30)
    draw.ellipse([
        center - head_radius + 2,
        center - head_radius * 1.5 + 2,
        center + head_radius + 2,
        center + head_radius * 0.5 + 2
    ], fill=shadow_color)
    
    return image

def create_assistant_avatar(size: int = 128) -> Image.Image:
    """Create an assistant avatar image.
    
    Args:
        size: Image size in pixels
        
    Returns:
        PIL Image object
    """
    # 创建新图片
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    draw.ellipse([0, 0, size-1, size-1], fill=(52, 168, 83, 255))
    
    # 绘制机器人图标
    center = size // 2
    radius = size // 4
    
    # 头部
    head_radius = radius * 1.2
    draw.ellipse([
        center - head_radius,
        center - head_radius * 1.5,
        center + head_radius,
        center + head_radius * 0.5
    ], fill=(255, 255, 255, 255))
    
    # 眼睛
    eye_radius = radius * 0.3
    eye_spacing = radius * 0.8
    # 左眼
    draw.ellipse([
        center - eye_spacing - eye_radius,
        center - head_radius * 0.8,
        center - eye_spacing + eye_radius,
        center - head_radius * 0.8 + eye_radius * 2
    ], fill=(52, 168, 83, 255))
    # 右眼
    draw.ellipse([
        center + eye_spacing - eye_radius,
        center - head_radius * 0.8,
        center + eye_spacing + eye_radius,
        center - head_radius * 0.8 + eye_radius * 2
    ], fill=(52, 168, 83, 255))
    
    # 天线
    antenna_width = radius // 4
    antenna_height = radius * 1.5
    # 天线杆
    draw.rectangle([
        center - antenna_width // 2,
        center - head_radius * 1.8,
        center + antenna_width // 2,
        center - head_radius * 1.2
    ], fill=(255, 255, 255, 255))
    # 天线球
    draw.ellipse([
        center - antenna_width,
        center - head_radius * 2,
        center + antenna_width,
        center - head_radius * 1.8
    ], fill=(255, 255, 255, 255))
    
    # 添加阴影效果
    shadow_color = (0, 0, 0, 30)
    draw.ellipse([
        center - head_radius + 2,
        center - head_radius * 1.5 + 2,
        center + head_radius + 2,
        center + head_radius * 0.5 + 2
    ], fill=shadow_color)
    
    return image

def main() -> None:
    """Main entry point."""
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 创建用户头像
    user_avatar = create_user_avatar()
    user_avatar.save(current_dir / "user.png")
    
    # 创建助手头像
    assistant_avatar = create_assistant_avatar()
    assistant_avatar.save(current_dir / "assistant.png")
    
    print("Avatar images created successfully!")

if __name__ == "__main__":
    main() 