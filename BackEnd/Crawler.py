# @Date    : 14:55 01/19/2022
# @Author  : ClassicalPi
# @FileName: Crawler.py
# @Software: PyCharm

import requests
import json
import re
import pymysql
import time
import random
import tqdm

api_key = '22d8fc87d6d44ae7ba1ab3131620f2c0'
person_detail_url = 'https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}&language=en-us'
movie_cast_url = 'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'
person_movie_detail_url = 'https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={api_key}&language=en-us'
all_movie_genres_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-us'

chinese_pattern = re.compile(u"[\u4e00-\u9fa5]+")   # 用于查找汉字，选取演员的中文名

# TODO 连接本地mysql的CBDB数据库
mysql_db = pymysql.connect(
    host="localhost",
    user="root",
    db="MovieKnowledge",
    use_unicode=True,
    charset="utf8mb4",
    password="888888"
)
mysql_cursor = mysql_db.cursor()

# TODO 插入语句模板
insert_person_command = 'insert into person (person_english_name, person_name, person_biography, person_birth_place, person_id, person_birth_day, person_death_day) values (%s, %s, %s, %s, %s, %s, %s)'
insert_movie_command = 'insert into movie (movie_title, movie_introduction, movie_rating, movie_id, movie_release_date) values (%s, %s, %s, %s, %s)'
insert_person_movie_command = 'insert into person_to_movie (person_id, movie_id) values (%s, %s)'
insert_movie_genre_command = 'insert into movie_to_genre (movie_id, genre_id) values (%s, %s)'
insert_genre_command = 'insert into genre (genre_id, genre_name) values (%s, %s)'


def get_all_genres():
    """
    获取所有的电影类型
    :return:
    """
    r = requests.get(all_movie_genres_url.format(api_key=api_key))
    json_result = json.loads(r.content)
    genres = json_result['genres']
    genre_list = list()

    for g in genres:
        genre_list.append((g['id'], g['name']))

    return genre_list


def get_movie_cast(movie_id):
    # type: (int) -> list
    """
    获取此电影所有参演演员的ID
    :param movie_id:
    :return:
    """
    cast_list = list()
    r = requests.get(movie_cast_url.format(movie_id=movie_id, api_key=api_key))
    json_result = json.loads(r.content)
    movie_cast = json_result['cast']

    for cast in movie_cast:
        cast_list.append(cast['id'])

    return cast_list


def get_person_detail(person_id):
    """
    获取该演员的基本信息
    :param person_id:
    :return:
    """
    detail_list = list()
    r = requests.get(person_detail_url.format(person_id=person_id, api_key=api_key))
    json_result = json.loads(r.content)

    try:
        detail_list.append(json_result['name'].strip())
    except KeyError:
        detail_list.append(None)

    exist_chinese_name = False
    for tmp in json_result['also_known_as']:
        if chinese_pattern.search(tmp):
            detail_list.append(tmp.strip())
            exist_chinese_name = True
            break

    if not exist_chinese_name:
        detail_list.append(None)

    try:
        detail_list.append(json_result['biography'].strip().replace('\n', ''))
    except KeyError:
        detail_list.append(None)

    try:
        detail_list.append(json_result['place_of_birth'])
    except KeyError:
        detail_list.append(None)

    detail_list.append(json_result['id'])

    try:
        detail_list.append(json_result['birthday'])
    except KeyError:
        detail_list.append(None)

    try:
        detail_list.append(json_result['deathday'])
    except KeyError:
        detail_list.append(None)

    return tuple(detail_list)


def get_person_movie_credits(person_id):
    """
    获取该演员参演的所有电影的基本信息
    :return:
    """
    movie_id_list = list()
    movie_detail_list = list()
    movie_genre_list = list()

    r = requests.get(person_movie_detail_url.format(person_id=person_id, api_key=api_key))
    json_result = json.loads(r.content)

    person_movies = json_result['cast']

    for movie in person_movies:
        detail_list = list()
        detail_list.append(movie['original_title'].strip())

        try:
            detail_list.append(movie['overview'].strip().replace('\n', ''))
        except KeyError:
            detail_list.append(None)

        try:
            detail_list.append(movie['vote_average'])
        except KeyError:
            detail_list.append(None)

        detail_list.append(movie['id'])

        try:
            detail_list.append(movie['release_date'])
        except KeyError:
            detail_list.append(None)

        movie_id_list.append(movie['id'])
        movie_detail_list.append(tuple(detail_list))

        single_movie_pair_list = list()
        for genre_id in movie['genre_ids']:
            single_movie_pair_list.append((movie['id'], genre_id))
        movie_genre_list.append(single_movie_pair_list)

    return movie_id_list, movie_detail_list, movie_genre_list


if __name__ == '__main__':
    crawled_person_id_set = set()  # 记录获取过的人物
    crawled_movie_id_set = set()  # 记录获取过的电影

    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    start_time = time.time()
    # TODO 获取所有的电影类型，存入genre表中
    all_movie_genres = get_all_genres()
    mysql_cursor.executemany(insert_genre_command, all_movie_genres)

    # Leonardo
    start_person_id,start_person_name = 6193, "Leonardo Dicaprio"

    person_detail = get_person_detail(start_person_id)

    print(f'插入{start_person_name}个人信息......')
    mysql_cursor.execute(insert_person_command, person_detail)
    print('插入成功......\n')

    movies_id, movies_detail, movies_genres = get_person_movie_credits(start_person_id)

    person_movie_id_pair = [(start_person_id, m) for m in movies_id]

    print(f'插入{start_person_name}出演的所有电影信息......')
    mysql_cursor.executemany(insert_movie_command, movies_detail)
    print('插入成功......\n')

    print(f'插入{start_person_name}与电影的id对......')
    mysql_cursor.executemany(insert_person_movie_command, person_movie_id_pair)
    print('插入成功......\n')

    print(f'插入{start_person_name}电影与类型的id对......')
    mg_pair = list()
    for mg in movies_genres:
        mg_pair.extend(mg)
    mysql_cursor.executemany(insert_movie_genre_command, mg_pair)
    print('插入成功......\n')

    crawled_person_id_set.add(start_person_id)  # 记录已存储的信息

    person_id_queue = set()

    # TODO 从 start_person_name 出演的电影当中获取所有演员的ID
    print(f'获取{start_person_name}参演电影的所有其他演员ID........')
    for m_id in movies_id:
        crawled_movie_id_set.add(m_id)

        for cast_id in get_movie_cast(m_id):
            person_id_queue.add(cast_id)
    print('获取成功......\n')

    # TODO 获取这些演员的基本信息，存入person表中，并获取每个演员出演的所有电影基本信息

    print('获取其他演员的基本信息及参演的所有电影的信息........')
    person_detail_list = list()
    person_movies_list = list()
    person_movie_pair_list = list()
    print('共有{0}个演员的信息需要获取。'.format(len(person_id_queue)-1))

    for index, p_id in enumerate(tqdm.tqdm(person_id_queue)):
        # print('获取第{0}个演员的基本信息和其参演的所有电影的信息。'.format(index+1))
        if p_id not in crawled_person_id_set:
            time.sleep(random.randrange(0, 15) / 10)
            person_detail_list.append(get_person_detail(p_id))
            movies_id, movies_detail, movies_genres = get_person_movie_credits(p_id)
            person_movies_list.append((movies_id, movies_detail, movies_genres))    # 添加当前演员出演的所有电影的信息
            person_movie_pair_list.extend([(p_id, m) for m in movies_id])   # 添加当前演员与其出演电影的id对
            crawled_person_id_set.add(p_id)
    print('获取成功......\n')

    movie_list = list()
    genre_pair_list = list()
    # TODO 保存这些演员出演的电影基本信息到movie表与movie_genre表中
    for person_movie in person_movies_list:
        movies_id, movies_detail, movies_genres = person_movie

        for index, m_id in enumerate(movies_id):
            if m_id not in crawled_movie_id_set:
                movie_list.append(movies_detail[index])
                genre_pair_list.extend(movies_genres[index])
                crawled_movie_id_set.add(m_id)

    mysql_cursor.executemany(insert_movie_command, movie_list)
    mysql_cursor.executemany(insert_person_command, person_detail_list)
    mysql_cursor.executemany(insert_movie_genre_command, set(genre_pair_list))
    person_movie_pair_list = list(set(person_movie_pair_list))
    for i in tqdm.tqdm(range(len(person_movie_pair_list))):
        try:
            mysql_cursor.execute(insert_person_movie_command,person_movie_pair_list[i])
        except Exception as e:
            print(e, person_movie_pair_list[i])
            continue
    # TODO 提交所有insert操作
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    mysql_db.commit()
    mysql_cursor.close()
    mysql_db.close()

    print('共花费时间{0}s'.format(time.time() - start_time))