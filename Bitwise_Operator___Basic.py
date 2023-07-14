'''
비트 연산자에 대한 개념을 익히고,
비트 연산자를 활용하는 다양한 방식들을 공부하기 위한 코드 파일

비트 연산자는 기본적으로 컴퓨터의 가장 기본적인 구조인 이진법에 기반하여 연산을 하는 작업이다.
'''

# binary in Python
denary = 13
binary_1 = bin(13) # 파이썬이 기본적으로 제공하는 함수인 bin을 통해 십진수를 이진수로 변환 가능
binary_2 = 0b1101 # 13의 이진수 표현 1101에 이진수임을 명시하기 위해 숫자 앞에 0b 입력 (binary의 'b')

print(denary, type(denary)) # 13 (int)
print(binary_1, type(binary_1)) # '0b1101' (str)
print(binary_2, type(binary_2)) # 이진수를 입력하게 되면 파이썬에서 자동으로 십진수로 변환하여 출력한다.


# int 함수의 활용
# 스트링 형태의 숫자를 실수형으로 바꿔주기 위한 함수 int
denary_str = '13'
denary_int = int(denary_str)

# 이진수가 스트링 형태로 주어졌을 경우
binary_str = '1101'
binary_int = int(binary_str, 2) # 입력 값으로 2를 추가 > 10진수로 변환되어 출력


# 비트 논리 연산자
'''
	비트 논리 연산자의 기본적인 개념은 자릿수 간의 비교이다.
	
	1. & (and)
		
		bin(0b1101 & 0b1001)의 의미는, 각 자릿수가 모두 1이면 1, 하나라도 0이면 0이다.

		a = 1 1 0 1
		b = 1 0 0 1
		>>> 1 0 0 1

		따라서 결과 값은 1001의 십진수 값인 9

	2. | (or)

		bin(0b1101 | 0b1001)의 의미는, 각 자릿수 중 하나라도 1이면 1, 둘 다 0이면 0이다.

		a = 1 1 0 1
		b = 1 0 0 1
		>>> 1 1 0 1

		따라서 결과 값은 1101의 십진수 값인 13

	3. ^ (xor)

		bin(0b1101 ^ 0b1001)의 의미는, 각 자릿수가 서로 다르면 1, 같으면 0이다.

		a = 1 1 0 1
		b = 1 0 0 1
		>>> 0 1 0 0

		따라서 결과 값은 0110의 십진수 값인 4

	4. ~ (not)

		bin(~0b1101)의 의미는, 각 자릿수의 비트를 반전
		!!!BUT!!! 간단하지가 않다!!!
		int 자료형의 경우 최상위 비트의 값을 음양 부호로 사용하기 때문에 not 연산을 시행할 경우 값의 +- 부호가 반전된다.

		'2의 보수' 개념

		a = 1 1 0 1 (13)
		>>> 0 0 1 0
		
		* 0 0 1 0 값을 변환-> 1을 빼주고 1의 보수를 취해준다. -> 1 1 1 0

		따라서 결과는 ... 졸라 복잡하네...
		https://jays-log1111.tistory.com/entry/4-2-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B9%84%ED%8A%B8%EC%97%B0%EC%82%B0%EC%9E%90-2%EC%9D%98-%EB%B3%B4%EC%88%98-%EA%B3%B5%EB%B6%80%ED%95%98%EA%B8%B0

		복습 꼭 필요!

		이해했으면, 나오는 값은 매우 간단하다.
		비트반전 출력값 = -(입력값+1)
'''

binary_1 = 0b1101
binary_2 = 0b1001

# &, |, ^, ~
result_1 = binary_1 & binary_2
result_2 = binary_1 | binary_2
result_3 = binary_1 ^ binary_2
result_4 = ~binary_1

print(result_1) # 9  (1001)
print(result_2) # 13 (1101)
print(result_3) # 4  (0100)
print(result_4) # -13(-1110)


# 시프트 연산자
# 비트를 입력한 수치만큼 왼쪽, 오른쪽으로 이동하는 연산
binary = 0b1101

l_shift = bin(binary << 2)
r_shift = bin(binary >> 1)

print(l_shift) # 110100 (왼쪽으로 두칸 이동하며 오른쪽에 00추가)
print(r_shift) # 110 (맨 오르쪽 1이 삭제)