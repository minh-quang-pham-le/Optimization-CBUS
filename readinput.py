def read_multiple_test_cases(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().strip().split("\n\n")  # Chia test cases dựa trên dòng trắng

    test_cases = []
    for block in lines:
        lines_in_block = block.strip().split("\n")  # Chia nhỏ từng dòng trong mỗi test case
        n, q = map(int, lines_in_block[0].split())  # Đọc n và q
        c = [list(map(int, line.split())) for line in lines_in_block[1:]]  # Đọc ma trận
        test_cases.append((n, q, c))  # Lưu test case vào danh sách
    
    return test_cases