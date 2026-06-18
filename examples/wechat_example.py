import os
import sys
import json
from pathlib import Path

# Add the project root to Python path so we can import src and examples
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from examples.main import main as run_agent

def run_wechat_agent():
    examples_dir = Path(__file__).parent
    
    # 优先使用 wechat_config.json，否则回退到默认的 config.json
    wechat_config_path = examples_dir / "wechat_config.json"
    default_config_path = examples_dir / "config.json"
    
    if wechat_config_path.exists():
        config_path = wechat_config_path
    elif default_config_path.exists():
        config_path = default_config_path
    else:
        print("Error: 在 examples 目录下未找到 wechat_config.json 或 config.json 配置文件。")
        sys.exit(1)
        
    print(f"正在从以下路径加载基础配置: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
        
    # 覆盖或注入微信自动化的关键配置
    if "agent" not in cfg:
        cfg["agent"] = {}
        
    cfg["agent"]["task"] = "打开微信(WeChat)，搜索并找到‘文件传输助手’，在输入框中输入‘hello’并发送该消息。"
    cfg["agent"]["use_skills"] = True
    cfg["agent"]["use_plan"] = True
    cfg["agent"]["skills_dir"] = "skills"
    
    # 创建临时的配置文件传递给主程序运行
    temp_config_path = examples_dir / "wechat_temp_config.json"
    print(f"正在生成临时微信运行配置: {temp_config_path}")
    with temp_config_path.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        
    try:
        # 调用 examples.main 中的主函数，并传入我们组装好的微信配置
        print("正在启动 TuriX Agent 执行微信发送消息任务...")
        run_agent(str(temp_config_path))
    finally:
        # 清理临时配置文件
        if temp_config_path.exists():
            temp_config_path.unlink()
            print("临时配置文件已清理完毕。")

if __name__ == "__main__":
    run_wechat_agent()
