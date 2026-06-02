import streamlit as st
# Giả sử bạn có hàm xử lý chính trong chat.py, ví dụ: process_chat
# from chat import process_chat 

st.set_page_config(page_title="Research Agent Eval", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ VinAI Research Agent")

# Khởi tạo bộ nhớ lưu lịch sử hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại lịch sử chat trên màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận lệnh mới từ người dùng
if user_input := st.chat_input("Nhập yêu cầu nghiên cứu của bạn..."):
    # Hiển thị câu hỏi của user
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Gọi Agent và hiển thị kết quả
    with st.chat_message("assistant"):
        with st.spinner("Agent đang tra cứu và phân tích..."):
            # Gọi hàm lõi của hệ thống Agent (bạn nối với hàm thực tế của nhóm tại đây)
            # final_response = process_chat(user_input)
            final_response = "Đây là kết quả phản hồi mẫu từ Agent. Hãy kết nối với hàm thực tế!"
            
            st.markdown(final_response)
    
    # Lưu câu trả lời của AI vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": final_response})