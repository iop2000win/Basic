# Categorical

sample_df = pd.DataFrame([
                            ['all', 'F', '07-12'],
                            ['all', 'F', '13-18'],
                            ['all', 'F', '19-24'],
                            ['all', 'F', '25-29'],
                            ['all', 'F', '30-34'],
                            ['all', 'F', '35-39'],
                            ['all', 'F', '40-44'],
                            ['all', 'F', '45-49'],
                            ['all', 'F', '50-59'],
                            ['all', 'F', '60-69'],
                            ['all', 'F', '70+'],
                            ['all', 'F', '<07'],
                            ['all', 'M', '07-12'],
                            ['all', 'M', '13-18'],
                            ['all', 'M', '19-24'],
                            ['all', 'M', '25-29'],
                            ['all', 'M', '30-34'],
                            ['all', 'M', '35-39'],
                            ['all', 'M', '40-44'],
                            ['all', 'M', '45-49'],
                            ['all', 'M', '50-59'],
                            ['all', 'M', '60-69'],
                            ['all', 'M', '70+'],
                            ['all', 'M', '<07'],
                            ['all', 'O', 'OTHER']
                        ],
                        columns = ['retailer', 'gender_code', 'birth_code'])

'''
단순 정렬이 아니라, 내가 원하는 순서대로 정렬 순서를 지정해주고 싶을 때, Categorical 데이터 타입을 활용한다.
'''
# 단순 정렬
display(sample_df.sort_values(['birth_code']))

# 카테고리 정렬 - '<07'이 '07-12'보다 앞으로 오도록
cate_sort = ['<07', '07-12', '13-18', '19-24', '25-29', '30-34', '35-39',
             '40-44', '45-49', '50-59', '60-69', '70+', 'OTHER']

sample_df['birth_code'] = pd.Categorical(sample_df['birth_code'], cate_sort, ordered = True)
display(sample_df.sort_values(['birth_code']))



# to_excel

df1 = pd.DataFrame()
df2 = pd.DataFrame()

output_path = './data/output.xlsx'

with pd.ExcelWriter(path) as writer:
    df1.to_excel(writer, sheet_name = 'sheet1', encoding = 'CP949', index = False)
    df2.to_excel(writer, sheet_name = 'sheet2', encoding = 'CP949', index = False)