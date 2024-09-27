import pendulum # type: ignore

def display_current_time():
    now = pendulum.now()  # Thời gian hiện tại
    print(f"Thời gian hiện tại: {now}")

    # Thời gian ở New York
    ny_time = now.in_timezone('America/New_York')
    print(f"Thời gian ở New York: {ny_time}")

if __name__ == "__main__":
    display_current_time()
