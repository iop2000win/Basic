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
기본적인 사용법
'''