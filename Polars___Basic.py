'''
Polars 라이브러리 활용에 대한 내용 정리

- 개요
Rust로 개발

멀티스레딩과 병렬 처리를 지원
단일 머신의 자원을 최대한 활용할 수 있도록 병렬 처리와 벡터화 연산을 통해 컬럼 기반 처리를 최적화


polars.DataFrame

- polars.LazyFrame
즉각적으로 연산을 하는 것이 아니라 쿼리 플랜만 담아두고 있다가 값이 필요할 때,
즉 구체화할 때 collect() 함수를 호출하여 연산하는 방식
'''

# Eager API - 즉각 연산
df = pl.read_parquet("predicted_data-1.parquet")
result = (
			df
				.filter(
						pl.col("distance") >= 2
						& pl.col("created_hour").is_in([11, 12, 13, 18, 19, 20])
						)
				.group_by("pickup_zone_id")
				.agg(
	    				pl.mean("delivery_time").alias("avg_delivery_time")
					)
		)

# Lazy API (scan_parquet 함수 사용과 마지막 collect 함수 호출이 유일한 차이) - Lazy 연산
df = pl.scan_parquet("predicted_data-1.parquet")
result = (
			df
				.filter(
						pl.col("distance") >= 2
						& pl.col("created_hour").is_in([11, 12, 13, 18, 19, 20])
						)
				.group_by("pickup_zone_id")
				.agg(
    					pl.mean("delivery_time").alias("avg_delivery_time")
					)
		).collect(streaming = False) # True로 할 경우, Out of Core 기능 사용

'''
어떤 최적화가 이루어지기 이렇게 큰 속도 차이가 날까?

간단하게 설명하자면,
즉각 연산의 경우, parquet 파일 전체를 읽어온 뒤에 필터 및 집계 연산을 진행한다.
반면에 Lazy 연산의 경우, parquet파일을 스캔만 한 상태에서 필터 및 집계 연산을 통해
추출해야할 데이터를 연산한 후에 필요한 데이터만 추출하는 방식이다.
'''


'''
streaming 기능
Out of Core(External memory 알고리즘)
'''



'''
Polars 문법
'''
import polars as pl
import pandas as pd
# ------------------------------------------------------------
# make and read data
#
# pl.DataFrame([value_list1, value_list2, ..., value_listN], schema = , orient = )
# pl.DataFrame({col_name: value_list, col_name: value_list, ...}, schema = )
# pl.read_csv()
# pl.read_excel()
# pl.read_parquet()
# pl.read_database(query = , connection = )
# ------------------------------------------------------------
'''

기본적으로 데이터의 값을 배열로 전달한다.
딕셔너리 형태로 테이블을 만들 때는 {key:value} = {컬럼명:컬럼값} 형태로 전달하면 된다.
각 컬럼에 대해서 데이터 타입을 지정하고 싶을 경우 schema 변수를 이용하면 된다.
값들만 배열로 전달할 경우에는 schema 변수를 통해 컬럼명 및 데이터 타입을 지정해줄 수 있다.
+) 배열만 전달할 경우 orient 변수를 통해 배열의 열기준/행기준을 정할수 있다.
   기본적으로는 열기준으로 처리된다.
'''
vendor_id = ['A', 'A', 'B', 'B', 'B']
passenger_count = [1, 1, 2, 2, 1]
trip_distance = [0.95, 1.2, 2.51, 2.9, 1.53]
payment_type = ['card', 'card', 'cash', 'cash', 'card']
total_amount = [14.3, 16.9, 34.6, 27.8, 15.2]

pl_df = pl.DataFrame([vendor_id, passenger_count, trip_distance, payment_type, total_amount])
'''
shape: (5, 5)
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ column_0 ┆ column_1 ┆ column_2 ┆ column_3 ┆ column_4 │
│ ---      ┆ ---      ┆ ---      ┆ ---      ┆ ---      │
│ str      ┆ i64      ┆ f64      ┆ str      ┆ f64      │
╞══════════╪══════════╪══════════╪══════════╪══════════╡
│ A        ┆ 1        ┆ 0.95     ┆ card     ┆ 14.3     │
│ A        ┆ 1        ┆ 1.2      ┆ card     ┆ 16.9     │
│ B        ┆ 2        ┆ 2.51     ┆ cash     ┆ 34.6     │
│ B        ┆ 2        ┆ 2.9      ┆ cash     ┆ 27.8     │
│ B        ┆ 1        ┆ 1.53     ┆ card     ┆ 15.2     │
└──────────┴──────────┴──────────┴──────────┴──────────┘
컬럼명이 없다.

+) 행기준으로 데이터 프레임을 만들 경우,
shape: (5, 5)
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ column_0 ┆ column_1 ┆ column_2 ┆ column_3 ┆ column_4 │
│ ---      ┆ ---      ┆ ---      ┆ ---      ┆ ---      │
│ str      ┆ str      ┆ str      ┆ str      ┆ str      │
╞══════════╪══════════╪══════════╪══════════╪══════════╡
│ A        ┆ A        ┆ B        ┆ B        ┆ B        │
│ 1        ┆ 1        ┆ 2        ┆ 2        ┆ 1        │
│ 0.95     ┆ 1.2      ┆ 2.51     ┆ 2.9      ┆ 1.53     │
│ card     ┆ card     ┆ cash     ┆ cash     ┆ card     │
│ 14.3     ┆ 16.9     ┆ 34.6     ┆ 27.8     ┆ 15.2     │
└──────────┴──────────┴──────────┴──────────┴──────────┘
'''

pl_df = pl.DataFrame(
						[vendor_id, passenger_count, trip_distance, payment_type, total_amount],
						schema = ['vendor_id', 'passenger_count', 'trip_distance', 'payment_type', 'total_amount']
					)
'''
shape: (5, 5)
┌───────────┬─────────────────┬───────────────┬──────────────┬──────────────┐
│ vendor_id ┆ passenger_count ┆ trip_distance ┆ payment_type ┆ total_amount │
│ ---       ┆ ---             ┆ ---           ┆ ---          ┆ ---          │
│ str       ┆ i64             ┆ f64           ┆ str          ┆ f64          │
╞═══════════╪═════════════════╪═══════════════╪══════════════╪══════════════╡
│ A         ┆ 1               ┆ 0.95          ┆ card         ┆ 14.3         │
│ A         ┆ 1               ┆ 1.2           ┆ card         ┆ 16.9         │
│ B         ┆ 2               ┆ 2.51          ┆ cash         ┆ 34.6         │
│ B         ┆ 2               ┆ 2.9           ┆ cash         ┆ 27.8         │
│ B         ┆ 1               ┆ 1.53          ┆ card         ┆ 15.2         │
└───────────┴─────────────────┴───────────────┴──────────────┴──────────────┘
'''

pl_df = pl.DataFrame(
						{
							'vendor_id': vendor_id,
							'passenger_count': passenger_count,
							'trip_distance': trip_distance,
							'payment_type': payment_type,
							'total_amount': total_amount
						},
						# schema = {
						# 			'vendor_id': str,
						# 			'passenger_count': int,
						# 			'trip_distance': float,
						# 			'payment_type': str,
						# 			'total_amount': float
						# }
				)
'''
해당 방법이 가장 활용도가 높을 것으로 보인다.

shape: (5, 5)
┌───────────┬─────────────────┬───────────────┬──────────────┬──────────────┐
│ vendor_id ┆ passenger_count ┆ trip_distance ┆ payment_type ┆ total_amount │
│ ---       ┆ ---             ┆ ---           ┆ ---          ┆ ---          │
│ str       ┆ i64             ┆ f64           ┆ str          ┆ f64          │
╞═══════════╪═════════════════╪═══════════════╪══════════════╪══════════════╡
│ A         ┆ 1               ┆ 0.95          ┆ card         ┆ 14.3         │
│ A         ┆ 1               ┆ 1.2           ┆ card         ┆ 16.9         │
│ B         ┆ 2               ┆ 2.51          ┆ cash         ┆ 34.6         │
│ B         ┆ 2               ┆ 2.9           ┆ cash         ┆ 27.8         │
│ B         ┆ 1               ┆ 1.53          ┆ card         ┆ 15.2         │
└───────────┴─────────────────┴───────────────┴──────────────┴──────────────┘
'''


# ------------------------------------------------------------
# 컬럼 선택
# df.select()
# pl.col()
# pl.col().exclude()
# df.drop()
# polars.selectors
# ------------------------------------------------------------
'''
컬럼을 선택하는 방법은 매우 다양하다.
pandas와 동일하게 대괄호를 통해 선택하는 것이 가능하다.
다만, polars는 체인 연산 및 선택과 연산을 한 번에 처리하는 것이 매우 편한데
대괄호 방식을 활용하면 이를 활용하는 것이 어렵다.
그러므로 단순히 원하는 컬럼만 선택해서 보고 싶을 경우에는 대괄호를 통한 선택이 간편하지만,
.select(pl.col()) 메서드를 활용하는 방법에 익숙해지는 것이 좋다.

pl.col()은 polars에서 컬럼을 나타내는 표현식인데 이를 활용해 단순한 선택과 기본 연산 뿐 아니라,
다양한 체인 연산과 함수 적용까지 가능하다.

select, drop 메서드는 새로운 데이터 프레임을 리턴하는 함수이다.
따라서 df 자체가 바뀌는 것이 아니므로 해당 결과로 데이터 프레임을 변경하고 싶을 경우,
변수에 해당 값을 다시 선언 해주어야 한다.
'''
print(pl_df[['vendor_id', 'passenger_count']])
print(pl_df.select(['vendor_id', 'passenger_count']))
print(pl_df.select(pl.col(['vendor_id', 'passenger_count'])))
print(pl_df.select(
					pl.col('vendor_id'),
					pl.col('passenger_count') # 각 컬럼에 대해서 메서드를 적용할 경우 컬럼을 이렇게 나열하면 유용하다.
				)
	)
# 모두 동일한 결과가 나온다.

# 모든 컬럼 선택 및 특정 컬럼 제외
print(pl_df)
print(pl_df.select('*'))
print(pl_df.select(pl.col('*')))
print(pl_df.select(pl.all()))

print(pl_df.select(pl.col('*').exclude(['payment_type', 'total_amount'])))
print(pl_df.select(pl.all().exclude('payment_type', 'total_amount'))) # 리스트로 감싸서 입력해도 되고, 그냥 나열해도 된다.
print(pl_df.drop(['payment_type', 'total_amount']))

# selector 활용하기
import polars.selectors as cs
print(cs.integer())
print(cs.string())
print(cs.numeric())
print(cs.float())

print(pl_df.select(pl.col(pl.Float64, pl.String)))
print(pl_df.select(cs.float(), cs.string()))
# 해당 데이터 타입을 가진 컬럼들만 선택

# 정규표현식 사용 가능 - It should start with '^' and end with '$'
print(pl_df.select(pl.col('^.*(amount|count)$')))


# ------------------------------------------------------------
# null 값 처리
# ------------------------------------------------------------
'''
컬럼별로 결측치 수를 확인하고, 결측치를 어떻게 처리할 것인지 결정할 수 있다.
'''
pl_null_df = pl.DataFrame({
    "vendor_id": ["A", "A", "B", None, "B"],
    "passenger_count": [1, None, None, 2, 1],
    "trip_distance": [0.95, 1.2, None, 2.9, 1.53],
    "payment_type": ["card", "card", None, None, "card"],
    "total_amount": [14.3, 16.9, None, 27.8, 15.2]
})

print(pl_null_df.null_count())
print(pl_null_df.select(pl.col('*').is_null()).sum())
print(pl_null_df.select(pl.col('*').is_null()))
'''
shape: (1, 5)
┌───────────┬─────────────────┬───────────────┬──────────────┬──────────────┐
│ vendor_id ┆ passenger_count ┆ trip_distance ┆ payment_type ┆ total_amount │
│ ---       ┆ ---             ┆ ---           ┆ ---          ┆ ---          │
│ u32       ┆ u32             ┆ u32           ┆ u32          ┆ u32          │
╞═══════════╪═════════════════╪═══════════════╪══════════════╪══════════════╡
│ 1         ┆ 2               ┆ 1             ┆ 2            ┆ 1            │
└───────────┴─────────────────┴───────────────┴──────────────┴──────────────┘

shape: (5, 5)
┌───────────┬─────────────────┬───────────────┬──────────────┬──────────────┐
│ vendor_id ┆ passenger_count ┆ trip_distance ┆ payment_type ┆ total_amount │
│ ---       ┆ ---             ┆ ---           ┆ ---          ┆ ---          │
│ bool      ┆ bool            ┆ bool          ┆ bool         ┆ bool         │
╞═══════════╪═════════════════╪═══════════════╪══════════════╪══════════════╡
│ false     ┆ false           ┆ false         ┆ false        ┆ false        │
│ false     ┆ true            ┆ false         ┆ false        ┆ false        │
│ false     ┆ true            ┆ true          ┆ true         ┆ true         │
│ true      ┆ false           ┆ false         ┆ true         ┆ false        │
│ false     ┆ false           ┆ false         ┆ false        ┆ false        │
└───────────┴─────────────────┴───────────────┴──────────────┴──────────────┘
'''

pl_null_df.fill_null()
pl_null_df.fill_null(pl.lit())
pl_null_df.select(pl.col('*').fill_null())

# strategy = 'forward', 'backward', 'min', 'max', 'mean', 'zero', 'one'
# pl.median() - 중간 값으로 널 값을 채우는 방법
# interpolate() - 보간법을 통해 널 값을 채우는 방법
pl_null_df.fill_null(strategy = 'forward') # 앞의 값으로 채우기
pl_null_df.fill_numm()


# ------------------------------------------------------------
# 기본 연산
# ------------------------------------------------------------




# ------------------------------------------------------------
# df.filter()
# ------------------------------------------------------------



# ------------------------------------------------------------
# df.with_columns()
# ------------------------------------------------------------



# ------------------------------------------------------------
# join(merge)
# ------------------------------------------------------------


# ------------------------------------------------------------
# group_by
# ------------------------------------------------------------