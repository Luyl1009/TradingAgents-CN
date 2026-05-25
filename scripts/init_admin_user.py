"""
初始化默认管理员用户
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.user_service import user_service
from app.models.user import UserCreate

async def create_default_admin():
    """创建默认管理员用户"""
    print("🔧 开始创建默认管理员用户...")
    
    try:
        # 检查 admin 用户是否已存在
        existing_user = await user_service.get_user_by_username("admin")
        
        if existing_user:
            print("✅ Admin 用户已存在")
            print(f"   用户名: {existing_user.username}")
            print(f"   邮箱: {existing_user.email}")
            print(f"   管理员: {existing_user.is_admin}")
            return
        
        # 创建 admin 用户
        print("📝 创建 admin 用户...")
        admin_user = await user_service.create_user(
            UserCreate(
                username="admin",
                email="admin@tradingagents.cn",
                password="admin123",
                is_admin=True
            )
        )
        
        if admin_user:
            print("✅ Admin 用户创建成功!")
            print(f"   用户名: {admin_user.username}")
            print(f"   邮箱: {admin_user.email}")
            print(f"   管理员: {admin_user.is_admin}")
            print("\n🔐 登录信息:")
            print("   用户名: admin")
            print("   密码: admin123")
            print("\n⚠️  请在首次登录后立即修改密码!")
        else:
            print("❌ Admin 用户创建失败")
            
    except Exception as e:
        print(f"❌ 创建过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭数据库连接
        await user_service.close()

if __name__ == "__main__":
    asyncio.run(create_default_admin())
