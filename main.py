import tkinter as tk
import time
import random

start_time = None
running = False
current_sentence_index = 0
total_time = 0
total_words = 0
total_accuracy = 0


test_texts = [
    "안녕하세요 지성스 입니다.",
    "오늘은 타자연습기를 만들어 봤습니다.",
    "생각보다 어렵네요.",
]



def start_timer(event):
    global start_time, running
    if not running:  # 타이머가 시작되지 않은 경우에만 시작
        start_time = time.time()
        running = True
        update_timer()

def update_timer():
    if running:
        elapsed_time = time.time() - start_time
        time_label.config(text=f"Time: {elapsed_time:.2f} seconds")
        # 100ms(0.1초)마다 update_timer 함수를 다시 호출
        time_label.after(100, update_timer)


def next_sentence():
    global current_sentence_index
    if current_sentence_index < len(test_texts) - 1:
        current_sentence_index += 1
        label.config(text=test_texts[current_sentence_index])
        entry.delete(0, tk.END)
        result_label.config(text="")
        time_label.config(text="Time: 0.00 seconds")
        start_timer(None)
    else:
        show_final_results()

def calculate_speed(event):
    global start_time, running, total_time, total_words, total_accuracy
    
    running = False  # 타이머 중지
    end_time = time.time() #종료시간
    elapsed_time = end_time - start_time #걸린시간
    total_time += elapsed_time

    typed_text  = entry.get()
    word_count = len(typed_text.split())
    total_words += word_count
    #분당 타이핑 속도 계산
    wpm = (word_count / elapsed_time) * 60

    # 정확도 계산
    accuracy = len([1 for i, c in enumerate(typed_text) if i < len(test_text) and c == test_text[i]]) / len(test_text)
    accuracy = accuracy * 100
    total_accuracy += accuracy

    result_label.config(text = f"타이핑 속도는 : 분당 {wpm:.2f} 입니다. 정확도는 : {accuracy:.2f}% 입니다.")
    time_label.config(text=f"Time taken: {elapsed_time:.2f} seconds")  # 시간 표시 추가
    start_time = None  # 타이머 초기화

    # 다음 문장으로 넘어가기
    next_sentence()

def show_final_results():
    global total_time, total_words, total_accuracy
    avg_wpm = (total_words / total_time) * 60
    avg_accuracy = total_accuracy / len(test_texts)
    
    final_result = f"Test completed!\nAverage Typing Speed: {avg_wpm:.2f} WPM\nAverage Accuracy: {avg_accuracy:.2f}%"
    result_label.config(text=final_result)
    entry.config(state="disabled")  # 입력 필드를 비활성화하여 더 이상 입력하지 않도록 설정


root = tk.Tk()
root.title("Typing sppd Tester")
root.geometry("600x400")

test_text = "안녕하세요 저는 지성스 입니다."

# label = tk.Label(root, text=test_text, font=("Arieal", 14))
# label.pack(pady=20)

#랜덤으로 첫 번째 문장 선택
random.shuffle(test_texts)
label = tk.Label(root, text=test_texts[current_sentence_index], font=("Arial", 14))
label.pack(pady=20)

entry = tk.Entry(root, width=50, font=("Arial", 14))
entry.pack(pady=20)

#

# 입력 필드에 이벤트 바인딩
entry.bind("<KeyPress>", start_timer)  # 키 입력이 시작되는 순간 타이머 시작
entry.bind("<Return>", calculate_speed)  # 엔터키가 눌리면 타이머 종료 및 속도 계산

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=20)

# 타이머 시간을 표시할 레이블
time_label = tk.Label(root, text="00:00", font=("Arial", 14))
time_label.pack(pady=20)



root.mainloop()

