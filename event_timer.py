import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta
import pygame.mixer
import tkinter.messagebox as messagebox

class EventTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Event Timer")
        self.root.attributes('-topmost', True)
        
        # メインフレーム
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        
        # コントロールフレーム
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack()
        
        # 音声初期化
        pygame.mixer.init()
        self.bell_sound = pygame.mixer.Sound("bell.wav")
        self.alarm_sound = pygame.mixer.Sound("alarm.wav")
        
        # タイマー状態
        self.is_running = False
        self.remaining_time = 0
        self.bell_time = 0
        self.presentation_time = 0
        self.qa_time = 0
        
        # 時間を秒に変換（小数点対応）
        self.bell_time = float(self.bell_time) * 60  # 分を秒に変換
        self.presentation_time = float(self.presentation_time) * 60
        self.qa_time = float(self.qa_time) * 60
        
        # 時間表示ラベル（初期状態）
        self.time_label = None
        self.create_normal_label()
        
        self.setup_ui()
        
    def setup_ui(self):
        # 時間設定フレーム
        settings_frame = ttk.LabelFrame(self.main_frame, text="タイマー設定", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # 呼び鈴時間設定
        ttk.Label(settings_frame, text="予備鈴時間（分）:").grid(row=0, column=0, pady=5)
        self.bell_entry = ttk.Entry(settings_frame, width=10)
        self.bell_entry.grid(row=0, column=1, pady=5)
        self.bell_entry.insert(0, "8")
        
        # 発表時間設定
        ttk.Label(settings_frame, text="発表時間（分）:").grid(row=1, column=0, pady=5)
        self.presentation_entry = ttk.Entry(settings_frame, width=10)
        self.presentation_entry.grid(row=1, column=1, pady=5)
        self.presentation_entry.insert(0, "10")
        
        # 質疑応答時間設定
        ttk.Label(settings_frame, text="質疑応答時間（分）:").grid(row=2, column=0, pady=5)
        self.qa_entry = ttk.Entry(settings_frame, width=10)
        self.qa_entry.grid(row=2, column=1, pady=5)
        self.qa_entry.insert(0, "15")
        
        # コントロールボタン
        control_frame = ttk.Frame(self.control_frame)
        control_frame.pack(pady=10)
        
        # スタートボタンの作成（インスタンス変数として保存）
        self.start_button = tk.Button(self.control_frame, text="開始", command=self.start_timer)
        self.start_button.pack()
        
        self.stop_button = ttk.Button(control_frame, text="停止", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=5)
        
        self.reset_button = ttk.Button(control_frame, text="リセット", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=5)
        
        # 表示モードのフラグ
        self.is_transparent_mode = False
    
    def start_timer(self):
        try:
            # 質疑応答時間（分）を取得（全体の時間）
            qa_time = float(self.qa_entry.get())
            # 発表時間（分）を取得（質疑応答時間までの残り時間）
            presentation_time = float(self.presentation_entry.get())
            # 予備鈴時間（分）を取得
            bell_time = float(self.bell_entry.get())
            
            # 質疑応答時間を初期の残り時間として設定（秒に変換）
            self.remaining_time = qa_time * 60
            
            # 各タイミングを質疑応答時間から差し引いて計算（秒単位）
            self.qa_time = (qa_time - presentation_time) * 60  # 発表終了時間
            self.bell_time = (qa_time - bell_time) * 60  # 予備鈴時間
            
            self.is_running = True
            self.is_transparent_mode = True
            self.show_transparent_mode()
            self.update_timer()
            
            # ボタンのテキストを更新
            self.start_button.config(text="停止")
            
        except ValueError:
            messagebox.showerror("エラー", "正しい時間を入力してください")
    
    def create_normal_label(self):
        # 既存のラベルがあれば削除
        if self.time_label is not None:
            self.time_label.destroy()
        
        # 通常モード用のラベルを作成
        self.time_label = tk.Label(
            self.main_frame,
            text="00:00",
            font=('Helvetica', 24)
        )
        self.time_label.pack()
    
    def create_outlined_label(self, parent, text, font_size, bg_color):
        # ラベルを格納するフレーム
        frame = tk.Frame(parent, bg=bg_color)
        frame.pack()
        
        # アウトライン用のラベル（8方向）
        outline_positions = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),           (1, 0),
            (-1, 1),  (0, 1),  (1, 1)
        ]
        
        outline_labels = []
        for x, y in outline_positions:
            label = tk.Label(
                frame,
                text=text,
                font=('Helvetica', font_size, 'bold'),  # 太字に変更
                fg='white',
                bg=bg_color
            )
            label.place(x=x, y=y)
            outline_labels.append(label)
        
        # メインのテキスト
        main_label = tk.Label(
            frame,
            text=text,
            font=('Helvetica', font_size, 'bold'),  # 太字に変更
            fg='black',
            bg=bg_color
        )
        main_label.place(x=0, y=0)
        
        return frame, main_label, outline_labels
    
    def show_transparent_mode(self):
        # 既存のラベルを削除
        if self.time_label is not None:
            self.time_label.destroy()
        
        # フレームを非表示
        self.main_frame.pack_forget()
        self.control_frame.pack_forget()
        
        # タイマー表示用のフレーム
        self.timer_frame = tk.Frame(self.root, bg='systemTransparent')
        self.timer_frame.pack(padx=10, pady=10)
        
        # 時間表示ラベル（灰色）
        self.time_label = tk.Label(
            self.timer_frame,
            text="00:00",
            font=('Helvetica', 48, 'bold'),
            fg='#666666',  # ダークグレー
            # または fg='gray40' でも可
            bg='systemTransparent',
        )
        self.time_label.pack()
        
        # ウィンドウスタイル
        self.root.overrideredirect(True)
        self.root.attributes('-transparent', True)
        self.root.attributes('-topmost', True)
        self.root.config(bg='systemTransparent')
        
        # イベントバインド
        self.time_label.bind('<Double-Button-1>', self.toggle_display_mode)
        # ドラッグとダブルクリックの機能を追加
        def start_move(event):
            self.x = event.x
            self.y = event.y

        def stop_move(event):
            self.x = None
            self.y = None

        def do_move(event):
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
        
        # イベントをバインド
        self.time_label.bind('<Button-1>', start_move)
        self.time_label.bind('<ButtonRelease-1>', stop_move)
        self.time_label.bind('<B1-Motion>', do_move)
    
    def show_normal_mode(self):
        # 既存のラベルを削除
        if self.time_label is not None:
            self.time_label.destroy()
        
        # 透過モードのフレーム削除
        if hasattr(self, 'timer_frame'):
            self.timer_frame.destroy()
        
        # ウィンドウスタイルを戻す
        self.root.overrideredirect(False)
        self.root.attributes('-transparent', False)
        self.root.config(bg='systemButtonFace')
        
        # フレームを再表示
        self.main_frame.pack(padx=10, pady=10)
        self.control_frame.pack()
        
        # 通常モード用のラベルを作成
        self.create_normal_label()
        
        # イベントバインド
        self.time_label.bind('<Double-Button-1>', self.toggle_display_mode)
    
    def toggle_display_mode(self, event=None):
        if self.is_running:  # タイマー進行中の場合のみ切り替え可能
            self.is_transparent_mode = not self.is_transparent_mode
            if self.is_transparent_mode:
                self.show_transparent_mode()
            else:
                self.show_normal_mode()
    
    def stop_timer(self):
        self.is_running = False
        self.is_transparent_mode = False
        self.show_normal_mode()
        
        # ボタンのテキストを「再開」に変更
        self.start_button.config(text="再開")
    
    def reset_timer(self):
        self.is_running = False
        self.remaining_time = 0
        self.time_label.config(text="00:00")
    
    def update_timer(self):
        if self.is_running and self.remaining_time >= 0:
            minutes = int(self.remaining_time // 60)
            seconds = int(self.remaining_time % 60)
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            
            # 質疑応答時間から各時間を引いた値と比較
            qa_time = float(self.qa_entry.get()) * 60  # 全体の時間（秒）
            bell_time = float(self.bell_entry.get()) * 60  # 呼び鈴時間（秒）
            presentation_time = float(self.presentation_entry.get()) * 60  # 発表時間（秒）
            
            # 呼び鈴アラーム（質疑応答時間 - 呼び鈴時間 = 残り時間）
            if self.remaining_time == (qa_time - bell_time):
                self.bell_sound.play()
            
            # 発表終了アラーム（質疑応答時間 - 発表時間 = 残り時間）
            if self.remaining_time == (qa_time - presentation_time):
                self.alarm_sound.play()
            
            # 質疑応答終了アラーム
            if self.remaining_time == 0:
                self.alarm_sound.play()
                self.stop_timer()
                return
            
            self.remaining_time -= 1
            self.root.lift()  # 最前面表示を維持
            self.root.after(1000, self.update_timer)
    
    def run(self):
        self.root.mainloop()

    def format_time(self, seconds):
        # 小数点以下の秒も含めて表示
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes:02d}:{remaining_seconds:05.2f}"

    def draw(self):
        # ... existing code ...
        
        # 残り時間の表示を更新
        elapsed = self.format_time(self.elapsed_time)
        bell = self.format_time(self.bell_time)
        presentation = self.format_time(self.presentation_time)
        qa = self.format_time(self.qa_time)
        
        # テキストの描画
        text_lines = [
            f"経過時間: {elapsed}",
            f"予備鈴: {bell}",
            f"発表時間: {presentation}",
            f"質疑応答: {qa}"
        ]
        # ... rest of the drawing code ...

    def toggle_topmost(self):
        # 現在の状態を取得して反転
        current_state = self.root.attributes('-topmost')
        self.root.attributes('-topmost', not current_state)

if __name__ == "__main__":
    app = EventTimer()
    app.run() 