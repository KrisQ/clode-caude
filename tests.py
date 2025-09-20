# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content
# from functions.write_file import write_file
from functions.run_python_file import run_python_file


def main():
    # first_test = get_files_info("calculator", ".")
    # print("Current dir debug")
    # print(first_test)
    # second_test = get_files_info("calculator", "pkg")
    # print("/pkg debug")
    # print(second_test)
    # third_test = get_files_info("calculator", "/bin")
    # print("/bin debug")
    # print(third_test)
    # fourth_test = get_files_info("calculator", "../")
    # print("../debug")
    # print(fourth_test)

    # test_1 = get_file_content("calculator", "main.py")
    # test_2 = get_file_content("calculator", "pkg/calculator.py")
    # test_3 = get_file_content("calculator", "/bin/cat")
    # test_4 = get_file_content("calculator", "pkg/does_not_exist.py")
    # print(test_1)
    # print(test_2)
    # print(test_3)
    # print(test_4)

    # test_1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # test_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # test_3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    #
    # print(test_1)
    # print(test_2)
    # print(test_3)

    test_1 = run_python_file("calculator", "main.py")
    test_2 = run_python_file("calculator", "main.py", ["3 + 5"])
    test_3 = run_python_file("calculator", "tests.py")
    test_4 = run_python_file("calculator", "../main.py")
    test_5 = run_python_file("calculator", "nonexistent.py")

    print(test_1)
    print(test_2)
    print(test_3)
    print(test_4)
    print(test_5)


if __name__ == "__main__":
    main()
