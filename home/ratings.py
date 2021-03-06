import pandas as pd
import pymysql
import os

conn=pymysql.connect(host='3.37.63.164',port=3306,user='root',password='Here!234',db='here_it_is')
search_history="select * from home_search_history"
product_info="select * from home_product_info"

product_result = pd.read_sql_query(product_info,conn)
product_result.to_csv(r'product_info.csv',index=False)

search_result = pd.read_sql_query(search_history,conn)
search_result.to_csv(r'search_history.csv',index=False)

conn.close()

ratings = pd.read_csv('search_history.csv')
# Surprise 모듈에서 csv파일을 읽어오도록 포맷을 변경해주어야 하기 위해서 따로 저장
# 이 때, index값과 Header(칼럼명)값들 없애주면서 저장시키기
ratings.to_csv('search_history_surprise.csv', index=False, header=False)

from surprise.dataset import DatasetAutoFolds
from surprise.dataset import Reader
from surprise import SVD

reader = Reader(line_format='user item rating', sep=',',
               rating_scale=(0.5, 5))

# DatasetAutoFolds 클래스를 사용해서 개별적으로 생성
# index와 header가 없는 상태로 재생성했던 search_history_surprise.csv파일에 기반
data_folds = DatasetAutoFolds(ratings_file='search_history_surprise.csv',
                             reader=reader)

# 위에서 개별적으로 생성한 csv파일을 학습데이터로 생성
trainset = data_folds.build_full_trainset()
algo = SVD(n_factors=50, n_epochs=20, random_state=42)
algo.fit(trainset)

# 제품에 대한 정보 데이터 로딩
products = pd.read_csv('product_info.csv')
ratings = pd.read_csv('search_history.csv')


def get_unseen_surprise(ratings, products, member_id):
    # 특정 유저가 본 product id들을 리스트로 할당
    seen_products = ratings[ratings['member_id']==member_id]['product_id'].tolist()
    # 모든 제품들의 product id들 리스트로 할당
    total_products = products['product_id'].tolist()
    
    # 모든 제품들의 product id들 중 특정 유저가 본 product id를 제외한 나머지 추출
    unseen_products = [products for products in total_products if products not in seen_products]
    #print(f'특정 {member_id}번 유저가 본 제품 수: {len(seen_products)}\n추천한 제품 개수: {len(unseen_products)}\n전체 영화수: {len(total_movies)}')
    
    return unseen_products

def recomm_product_by_surprise(algo, member_id, unseen_movies, top_n=5):
    # 알고리즘 객체의 predict()를 이용해 특정 userId의 평점이 없는 제품들에 대해 평점 예측
    predictions = [algo.predict(str(member_id), str(product_id)) for product_id in unseen_movies]
    
    # predictions는 Prediction()으로 하나의 객체로 되어있기 때문에 예측평점(est값)을 기준으로 정렬해야함
    # est값을 반환하는 함수부터 정의. 이것을 이용해 리스트를 정렬하는 sort()인자의 key값에 넣어주자!
    def sortkey_est(pred):
        return pred.est
    
    # sortkey_est함수로 리스트를 정렬하는 sort함수의 key인자에 넣어주자
    # 리스트 sort는 디폴트값이 inplace=True인 것처럼 정렬되어 나온다. reverse=True가 내림차순
    predictions.sort(key=sortkey_est, reverse=True)
    # 상위 n개의 예측값들만 할당
    top_predictions = predictions[:top_n]
    
    # top_predictions에서 product id, rating, product name 각 뽑아내기
    top_product_ids = [int(pred.iid) for pred in top_predictions]
    top_product_ratings = [pred.est for pred in top_predictions]
    top_product_titles = products[products.product_id.isin(top_product_ids)]['product_nm']
    # 위 3가지를 튜플로 담기
    # zip함수를 사용해서 각 자료구조(여기선 리스트)의 똑같은 위치에있는 값들을 mapping
    # zip함수는 참고로 여러개의 문자열의 똑같은 위치들끼리 mapping도 가능!
    top_product_preds = [(ids, rating, product_nm) for ids, rating, product_nm in zip(top_product_ids, top_product_ratings, top_product_titles)]
    
    return top_product_preds


unseen_lst = get_unseen_surprise(ratings, products, 'rudckf113')
top_products_preds = recomm_product_by_surprise(algo, 'rudckf113', unseen_lst,top_n=5)

print()
print('#'*8,'rudckf113 님의 Top-5 추천제품 리스트','#'*8)

# top_products_preds가 여러가지의 튜플을 담고 있는 리스트이기 때문에 반복문 수행
for top_product in top_products_preds:
    print('* 추천 제품 이름: ', top_product[2])
    print('* 해당 제품의 예측평점: ', top_product[1])
    print()
