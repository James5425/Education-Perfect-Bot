from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

# view https://dev.to/ruthmoog/dealing-with-error-chromedriver-cannot-be-opened-because-the-developer-cannot-be
# -verified-1897 if any issues with apple quarantine
#https://app.educationperfect.com/app/Japanese/6230459/4299030/list-starter
# Path to webdriver
try:
    driver = webdriver.Chrome('ENTER THE PATH TO THR SELENIUM DRIVER DOWNLOAD FROM https://chromedriver.chromium.org/home')
except WebDriverException:
    print("You need to download the webdriver for your computer and then add it to PATH")
    exit()

# Load Website
website = input("Enter start page URL (This is the page with all the questions and answers)\n>")

driver.get(website)

# Login Info
username = input("Enter EP Username\n>")
password = input("Enter EP Password\n>")

# Stored Questions and Answer
answers = []
questions = []

# Counter for each questions
i = 1

# Page counter

a = 1

g = 1

# Logs into EP
def login(u, p):
    try:
        time.sleep(3)
        driver.find_element_by_id("login-username").send_keys(u)
        driver.find_element_by_id("login-password").send_keys(p)
        driver.find_element_by_id("login-submit-button").click()
    except NoSuchElementException:
        time.sleep(1)
        login(username, password)


# How many pages of questions?
def page_numbers():
    global pages
    try:
        pages = int(driver.find_element_by_xpath(
            '/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div[2]/div['
            '1]/div[2]/div/div[2]/b[2]').text)
        pages += 1
    except NoSuchElementException:
        pages = 1

    return pages


def infinit():

    try:
        time.sleep(3)

        # Scroll Page and Selects option as infinite
        element = driver.find_element_by_xpath(
            "/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div[1]/div[3]/div["
            "1]/div[3]/ul/li[5]/div")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element.click()
        time.sleep(2)
    except NoSuchElementException:
        driver.find_element_by_xpath('/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div[1]/div[3]/div[1]/div[2]/ul/li[5]/div').click()
        time.sleep(2)


def one_page(i1, readOrWrite):
    while True:
        try:
            # Adds the questions and answers into arrays

            question = driver.find_element_by_xpath(
                f'/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div['
                f'2]/div[4]/div[1]/div[1]/div[{i1}]/div[1]/div[1]').get_attribute(
                'textContent').strip()


            # If there is a ; the question delete it and everything before it as EP Bot doesn't read this properly
            for x in question:
                if x == ";":
                    sep = ';'
                    question = question.split(sep, 1)[1].strip()
                else:
                    question = question

            #When doing spelling questions have a double space added on the front page but not during questioning
            while '  ' in question:
                question = question.replace('  ', ' ')
                print(question)


            answer = driver.find_element_by_xpath(
                f'/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div['
                f'2]/div[4]/div[1]/div[1]/div[{i1}]/div[1]/div[2]').get_attribute(
                'textContent').strip()
            print(question)
            print(answer)

            if readOrWrite == 2:
                for b in answer:
                    if b == ";":
                        sep = ";"
                        answer = answer.split(sep, 1)[1].strip()
                    else:
                        answer = answer
            else:
                pass

            questions.append(question)
            answers.append(answer)
            i1 += 1
        except:
            # For when there are no more questions
            break

def more_than_one_page(i1, a1, pages, readOrWrite):
    b = 1

    while b == 1:
        try:
            # Adds the questions and answers into arrays
            question = driver.find_element_by_xpath(
                f'/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div['
                f'2]/div[4]/div[1]/div[1]/div[{i1}]/div[1]/div[1]').get_attribute(
                'textContent').strip()

            # If there is a ; the question delete it and everything before it as EP Bot doesn't read this properly
            for x in question:
                if x == ";":
                    sep = ';'
                    question = question.split(sep, 1)[1].strip()
                else:
                    question = question

            # When doing spelling questions have a double space added on the front page but not during questioning
            while '  ' in question:
                question = question.replace('  ', ' ')
                print(question)

            answer = driver.find_element_by_xpath(
                f'/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div['
                f'2]/div[4]/div[1]/div[1]/div[{i1}]/div[1]/div[2]').get_attribute(
                'textContent').strip()

            if readOrWrite == 2:
                for b in answer:
                    if b == ";":
                        sep = ";"
                        answer = answer.split(sep, 1)[1].strip()
                    else:
                        answer = answer
            else:
                pass

            questions.append(question)
            answers.append(answer)
            i1 += 1
        except:
            # For when there are no more questions
            driver.find_element_by_xpath(
                '/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div['
                '2]/div[1]/div[2]/div/div[3]').click()
            a1 += 1
            i1 = 1
            time.sleep(3)
            if a1 == pages:
                b = 2


def start():
    # Starts EP Answering
    time.sleep(4)
    driver.find_element_by_id("start-button-main").click()
    time.sleep(2)


def answer():
    g = 1

    while True:

        try:

            try:
                # Reads questions
                task_question = driver.find_element_by_xpath(
                    '/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div[1]/ui-view/div[1]/div[2]/div/div/div['
                    '1]/div[2]/div/div[2]/div[2]/span[2]/span').text

                if task_question == '':
                    task_question = driver.find_element_by_xpath('/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div[1]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[2]/span[2]').text
                print(task_question)
                try:
                    # Finds answer to question
                    task_answer_index = questions.index(task_question)
                    task_answer = (answers[task_answer_index])
                except:
                    # Finds answer to question
                    task_answer_index = answers.index(task_question)
                    task_answer = (questions[task_answer_index])

                # Removes everything in the answer after ; as EP bot does not need this
                try:
                    sep = ';'
                    stripped = task_answer.split(sep, 1)[0]
                    # Enters answer into text box
                    enter_answer = driver.find_element_by_xpath(
                        '/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div[1]/ui-view/div[1]/div[2]/div/div/div['
                        '2]/div[2]/game-lp-answer-input/div/div[2]/input')
                    enter_answer.send_keys(stripped)
                    enter_answer.send_keys(Keys.ENTER)
                    prev_answer = stripped
                    if read_write == 2:
                        if driver.find_element_by_xpath('/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div[1]/ui-view/div[1]/div[2]/div/div/div[''1]/div[2]/div/div[2]/div[2]/span[2]/span').text == task_question:
                            enter_answer.send_keys(Keys.ENTER)
                        else:
                            pass
                    else:
                        pass
                    time.sleep(3)
                except NoSuchElementException:
                    print("All Questions Finished")
            except NoSuchElementException:
                g += 1
                if g != 5:
                    answer()
                else:
                    break
        except RecursionError:
            driver.find_element_by_xpath('/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div[1]/div/div/div[2]/button[2]').click()
            time.sleep(1)
            answer()

def reading_or_writing():
    global read_write
    read_write = int(input("Would you like the EP Bot to do the reading or writing section? (Reading = 1 / Writing = 2)\n>"))
    if read_write == 1:
        pass
    elif read_write == 2:
        driver.find_element_by_xpath('/html/body/main/div[3]/div/student-app-wrapper/div[1]/div[2]/div/ui-view/div/div[2]/div/div[1]/div[3]/div[1]/div[2]/ul/li[4]').click()
    else:
        print("Please Enter a valid option")
    return read_write

def main(i1, a1):
    login(username, password)
    time.sleep(3)

    reading_or_writing()
    time.sleep(1)
    infinit()
    page_numbers()

    if pages == 1: # For when only one page of questions
        one_page(i1, read_write)

    elif pages > 1:  # For when more than one page of questions
        more_than_one_page(i1, a1, pages, read_write)

    start()
    time.sleep(2)
    answer()


if __name__ == '__main__':
    main(i, a)
