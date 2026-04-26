import streamlit as st
import pandas as pd
import os
from datetime import datetime
import requests

# ---------- 页面配置 ----------
st.set_page_config(page_title="Doorslamer", layout="centered")

# ---------- 样式 ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
* {
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.4px;
}
body {
    background-color: #0f172a;
    color: #e2e8f0;
}
.stTextInput input, .stTextArea textarea {
    background-color: #1e293b !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
}
.stButton button {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}
div[data-testid="stAlert"] {
    background-color: #1e293b !important;
    border: none !important;
    color: white !important;
}
hr {
    border-color: #1e293b !important;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ========== 顶部完整文字 ==========
st.markdown("""
# 🧊 Welcome to Doorslamer!

这档播客想做的事情很简单：

在不打扰彼此生活的前提下，重新建立一种轻松的连接。

我们可以聊：
- 最近在面对什么新的课题
- 还会回忆的过去，正在期盼的未来
- 在不同城市、不同环境下，生活如何展开
- 那些一个人思考过很久的问题，有没有新的答案
- 当下的人际关系，新朋友与老朋友
- 喜悦、低落、平静、焦虑、希望、迷茫
- 以及一切你愿意分享的话题

我们相信一种“长期主义”的关系：
不需要频繁出现，但可以在不同阶段重新对话。

与你开启一段聊天对我而言有点困难，所以想短暂地闯入你的社交区域，好奇你最近在忙什么，
这个播客或许可以陪你暂时抽身于日复一日的生活，
或许开启一段新的旅程，有幸可以为你记录下属于你的奥德赛时期，也来一起拼凑我们乱七八糟的当下。

而对话的意义，是让这些问题不再只能一个人面对。

无关时间地点，去除社交环境，
期待再次与你会面，也欢迎带上你的朋友。

时间会帮我们把很多事情串联起来
就像老薛说的：别有压力，我只想见见你

Tips：
落笔须知！当我收到你温暖的答复时，我会主动前来与你聊聊天，无论是否与播客相关都可以。
如果你还没有准备好，我会在这里等你，缘分未至，但以上，见字如面。
""")

st.markdown("---")

# ========== 【后台密码】自己修改这里 ==========
ADMIN_PASSWORD = "wyy512"

# ========== 微信推送（可选） ==========
SEND_KEY = "SCT340272TkNKeH36CrxB4rZy6qBjbP0xE"  # 不填就不推送

def send_wechat_msg(name):
    if not SEND_KEY:
        return
    try:
        url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"
        data = {
            "title": "✅ 播客问卷新提交",
            "desp": f"昵称：{name}\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }
        requests.post(url, data=data, timeout=5)
    except:
        pass

# ========== 数据文件 ==========
DATA_FILE = "../answers.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "time", "name", "mbti", "major", "concern","city",
        "want_to_do", "want_to_go", "future_topic"
    ])
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# ========== 私密后台入口 ==========
with st.expander("🔐 管理员后台查看数据"):
    input_pwd = st.text_input("请输入管理员密码", type="password")
    if input_pwd == ADMIN_PASSWORD:
        st.success("✅ 身份验证成功，以下是完整数据")
        df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("💾 下载完整CSV", csv, "播客数据.csv", "text/csv")
    elif input_pwd != "":
        st.error("❌ 密码错误")

st.markdown("---")

# ========== 读取数据 & 显示人数 ==========
df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
st.subheader("📊 在你犹豫的时候")
st.markdown(f"**已有 {len(df)} 位朋友留下了自己的故事**")

st.markdown("---")

# ========== 一人只能提交一次 ==========
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.subheader("✍️ 只有你是天蓝色")

if st.session_state.submitted:
    st.success("✅ 你已经提交过啦，感谢你的分享！")
else:
    with st.form("form"):
        name = st.text_input("我记得你的名字是：")
        mbti = st.text_input("我还不知道你的MBTI是：")
        major = st.text_input("你一定对这个专业了如指掌了：")
        concern = st.text_input("总有些问题不断浮现在你的脑海：")
        city = st.text_input("你邂逅了哪个有趣的城市:")
        want_to_do = st.text_input("你的空闲时光总是用来：")
        want_to_go = st.text_input("你一定要去看看那里的风景：")
        future_topic = st.text_input("几年之后，你还会回忆起这个话题：")

        submitted = st.form_submit_button("提交记录")

        if submitted:
            name = name.strip()
            if not name:
                st.warning("请填写昵称")
            elif name in df["name"].astype(str).values:
                st.warning("该昵称已提交过，每人仅限一次")
            else:
                new_row = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": name,
                    "mbti": mbti.strip().upper(),
                    "major": major,
                    "concern": concern,
                    "city": city,
                    "want_to_do": want_to_do,
                    "want_to_go": want_to_go,
                    "future_topic": future_topic
                }
                new_df = pd.DataFrame([new_row])
                updated = pd.concat([df, new_df], ignore_index=True)
                updated.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

                send_wechat_msg(name)

                st.session_state.submitted = True
                st.success("✅谢谢你的用心参与，给我一点时间准备，请等待我的“打扰”！")
                st.balloons()
                st.rerun()
