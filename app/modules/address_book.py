from flask import Flask, request, render_template, session, jsonify, redirect
from bson.objectid import ObjectId
import json
import math
import re
import modules.mongo_connection

email_pattern = r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$"

def ab_list(page=1):
    (db, connection) = modules.mongo_connection.getDB('test')
    output = {
        'page_name': 'ab-list',
        'page_title': '列表 - 通訊錄',
        'totalRows': 0,   # 總筆數
        'perPage': 3,     # 每一頁最多幾筆
        'totalPages': 0,  # 總頁數
        'page': page,     # 用戶要查看的頁數
        'rows': [],       # 當頁的資料
    }
    output['totalRows']  = db.address_book.count_documents({})
    output['totalPages'] = math.ceil(output['totalRows']/output['perPage'])
    output['page'] = 1 if page < 1 else page
    if output['page'] > output['totalPages']:
        output['page'] = output['totalPages']
    if output['totalRows']==0:
        output['rows'] = []
    else:
        cursor = db.address_book.find({},
                        sort=[('_id', -1)],
                        skip=(output['page']-1) * output['perPage'],
                        limit=output['perPage']
                    )
        for doc in cursor:
            print(doc)
            doc['_id'] = str(doc['_id'])
            output['rows'].append(doc)
    return render_template('address-book/list.html', **output)

def ab_edit_get(_id):
    (db, connection) = modules.mongo_connection.getDB('test')
    try:
        oid = ObjectId(_id)
    except:
        return redirect("/address-book/list/1", code=302)

    row = db.address_book.find_one({'_id': oid})
    row['_id'] = _id  # 使用字串
    if not row:
        return redirect("/address-book/list/1", code=302)
    else:
        row['page_name'] = 'ab_edit'
        row['page_title'] = '修改 - 通訊錄'
        return render_template('address-book/edit.html', **row)

def ab_edit_post():
    output = {
        'success': False,
        'error': '',
    }
    if len(request.form.get('name')) < 2:
        output['error'] = '姓名字元長度太短'
        return output

    email_match = re.search(email_pattern, request.form.get('email'), re.I)
    if not email_match:
        output['error'] = 'Email 格式錯誤'
        return output

    (db, connection) = modules.mongo_connection.getDB('test')
    doc = request.form.to_dict()
    _id = doc['_id']
    del doc['_id']
    rr = db.address_book.replace_one({'_id': ObjectId(_id)}, doc)
    # print(rr) # pymongo.results.UpdateResult
    if rr.modified_count==1:
        output['success'] = True
    else:
        output['error'] = '資料沒有變更';

    return output

def ab_add_get():
    output = {
        'page_name': 'ab_add',
        'page_title': '新增 - 通訊錄',
    }
    return render_template('address-book/add.html', **output)

def ab_add_post():
    output = {
        'success': False,
        'error': '',
    }
    if len(request.form.get('name')) < 2:
        output['error'] = '姓名字元長度太短'
        return output
    
    email_match = re.search(email_pattern, request.form.get('email'), re.I)
    if not email_match:
        output['error'] = 'Email 格式錯誤'
        return output

    (db, connection) = modules.mongo_connection.getDB('test')
    doc = request.form.to_dict()
    rr = db.address_book.insert_one(doc)
    print(dir(rr))  # InsertOneResult
    if rr.inserted_id:
        output['success'] = True
    else:
        output['error'] = '資料沒有新增';
    return output
 