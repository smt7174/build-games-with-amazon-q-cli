#!/usr/bin/env python3
"""
時限爆弾ゲーム
エレメカゲームの「時限爆弾ゲーム」をコマンドラインで再現したゲームです。
プレイヤーは制限時間内に爆弾を解除するために正しい操作を行う必要があります。
"""

import random
import time
import os
import sys
import threading
from ascii_art import get_bomb_art, get_explosion_art, get_defused_art, get_timer_art, get_title_art

class TimeBombGame:
    def __init__(self, difficulty='normal'):
        # 難易度に応じて設定を変更
        if difficulty == 'easy':
            self.time_limit = 90  # 制限時間（秒）
            self.wires = ["赤", "青", "黄"]
            self.code_length = 3
        elif difficulty == 'hard':
            self.time_limit = 45  # 制限時間（秒）
            self.wires = ["赤", "青", "黄", "緑", "白", "黒", "紫"]
            self.code_length = 5
        else:  # normal
            self.time_limit = 60  # 制限時間（秒）
            self.wires = ["赤", "青", "黄", "緑", "白"]
            self.code_length = 4
            
        self.remaining_time = self.time_limit
        self.correct_wire = random.choice(self.wires)
        
        # 難易度に応じてコードの桁数を変更
        min_code = 10 ** (self.code_length - 1)
        max_code = (10 ** self.code_length) - 1
        self.correct_code = str(random.randint(min_code, max_code))
        
        self.game_over = False
        self.win = False
        self.timer_thread = None
        self.difficulty = difficulty
        
    def clear_screen(self):
        """画面をクリアする"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_bomb(self):
        """爆弾の状態を表示する"""
        self.clear_screen()
        print(get_title_art())
        print("\n" + "=" * 50)
        print("  時限爆弾ゲーム  ".center(50, "="))
        print("=" * 50 + "\n")
        
        # 残り時間の表示
        print(f"残り時間: {self.remaining_time}秒")
        
        # 爆弾の表示
        print(get_bomb_art())
        print("\n" + "-" * 40)
        print("  爆弾  ".center(40))
        print("-" * 40)
        print("\n配線:")
        for wire in self.wires:
            print(f" - {wire}色のワイヤー")
        print("\n数字キーパッド: [0-9]")
        print("-" * 40 + "\n")
        
    def countdown(self):
        """カウントダウンタイマー"""
        while self.remaining_time > 0 and not self.game_over and not self.win:
            time.sleep(1)
            self.remaining_time -= 1
            self.display_bomb()
            
            if self.remaining_time <= 0:
                self.game_over = True
                self.display_game_over()
                
    def start_timer(self):
        """タイマーをスタートする"""
        self.timer_thread = threading.Thread(target=self.countdown)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
    def display_game_over(self):
        """ゲームオーバー画面を表示"""
        self.clear_screen()
        print("\n" + "=" * 50)
        print("  ゲームオーバー  ".center(50, "="))
        print("=" * 50 + "\n")
        print(get_explosion_art())
        print("💥 爆弾が爆発しました！ 💥".center(50))
        print(f"\n正解は:")
        print(f" - 切るべきワイヤー: {self.correct_wire}色")
        print(f" - 解除コード: {self.correct_code}")
        print("\n" + "=" * 50)
        
    def display_win(self):
        """勝利画面を表示"""
        self.clear_screen()
        print("\n" + "=" * 50)
        print("  爆弾解除成功！  ".center(50, "="))
        print("=" * 50 + "\n")
        print(get_defused_art())
        print("🎉 おめでとうございます！爆弾の解除に成功しました！ 🎉".center(50))
        print(f"\n残り時間: {self.remaining_time}秒")
        print("\n" + "=" * 50)
        
    def cut_wire(self, wire_color):
        """ワイヤーを切る"""
        if wire_color == self.correct_wire:
            print(f"\n{wire_color}色のワイヤーを切りました。")
            print("最初のステップ成功！次は解除コードを入力してください。")
            return True
        else:
            self.game_over = True
            print(f"\n間違ったワイヤーを切りました！爆弾が起動します...")
            time.sleep(1)
            self.display_game_over()
            return False
            
    def enter_code(self, code):
        """解除コードを入力する"""
        if code == self.correct_code:
            self.win = True
            self.display_win()
            return True
        else:
            self.game_over = True
            print("\n間違ったコードを入力しました！爆弾が起動します...")
            time.sleep(1)
            self.display_game_over()
            return False
            
    def play(self):
        """ゲームを開始する"""
        self.display_bomb()
        self.start_timer()
        
        # 最初のステップ：ワイヤーを切る
        wire_cut = False
        while not wire_cut and not self.game_over and self.remaining_time > 0:
            try:
                wire_color = input("\nどの色のワイヤーを切りますか？ (色を入力): ")
                if wire_color in self.wires:
                    wire_cut = self.cut_wire(wire_color)
                else:
                    print(f"有効な色を入力してください: {', '.join(self.wires)}")
            except KeyboardInterrupt:
                print("\nゲームを終了します...")
                sys.exit(0)
                
        # 次のステップ：解除コードを入力
        if wire_cut and not self.game_over:
            while not self.win and not self.game_over and self.remaining_time > 0:
                try:
                    code = input(f"\n{self.code_length}桁の解除コードを入力してください: ")
                    if len(code) == self.code_length and code.isdigit():
                        self.enter_code(code)
                    else:
                        print(f"{self.code_length}桁の数字を入力してください。")
                except KeyboardInterrupt:
                    print("\nゲームを終了します...")
                    sys.exit(0)
        
        # ゲーム終了を待つ
        if self.timer_thread:
            self.timer_thread.join()
            
        # もう一度プレイするか尋ねる
        play_again = input("\nもう一度プレイしますか？ (y/n): ")
        if play_again.lower() == 'y':
            difficulty = self.select_difficulty()
            new_game = TimeBombGame(difficulty)
            new_game.play()
        else:
            print("ゲームを終了します。ありがとうございました！")
            
    def select_difficulty(self):
        """難易度を選択する"""
        print("\n難易度を選択してください:")
        print("1. 簡単 (90秒、3色のワイヤー、3桁のコード)")
        print("2. 普通 (60秒、5色のワイヤー、4桁のコード)")
        print("3. 難しい (45秒、7色のワイヤー、5桁のコード)")
        
        while True:
            try:
                choice = input("選択 (1-3): ")
                if choice == '1':
                    return 'easy'
                elif choice == '2':
                    return 'normal'
                elif choice == '3':
                    return 'hard'
                else:
                    print("1から3の数字を入力してください。")
            except KeyboardInterrupt:
                print("\nゲームを終了します...")
                sys.exit(0)

def main():
    """メイン関数"""
    print(get_title_art())
    print("時限爆弾ゲームへようこそ！")
    print("あなたは爆弾処理班です。制限時間内に爆弾を解除してください。")
    print("爆弾を解除するには、正しいワイヤーを切り、解除コードを入力する必要があります。")
    print("\n準備はいいですか？")
    input("ゲームを開始するには Enter キーを押してください...")
    
    # 難易度選択
    difficulty = TimeBombGame('normal').select_difficulty()
    game = TimeBombGame(difficulty)
    game.play()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nゲームを終了します...")
        sys.exit(0)
