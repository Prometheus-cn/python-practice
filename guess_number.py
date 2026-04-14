import random

def guess_number(max_attempts=5):
    secret = random.randint(1, 100)
    attempts = 0
    print(f"一个1-100之间的整数，你有{max_attempts}机会猜对")

    while attempts < max_attempts:
        try:
            guess = int(input(f"第{attempts+1}次猜测: "))
        except ValueError:
            print("请输入有效整数！")
            continue

        attempts += 1

        if guess < secret:
            print("数字太小了！")
        elif guess > secret:
            print("数字太大了")
        else:
            print(f"恭喜你猜对了！答案就是{secret}")
            break
    else:
        print(f"很遗憾，{max_attempts}次机会用完了。答案是{secret}")

if __name__ == "__main__":
    guess_number()