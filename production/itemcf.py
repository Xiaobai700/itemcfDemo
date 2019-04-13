from __future__ import division
import sys
sys.path.append("../datautil")
import dataUtil.reader as reader
import math
import operator


def base_contribute_score():
    return 1


def update_one_contribute_score(user_tatal_click_num):
    return 1/math.log10(1+user_tatal_click_num)

def update_two_contribute_score(click_time_one,click_time_two):
    delata_time = abs(click_time_one-click_time_two)
    #让它变成天的概念
    total_sec = 60*60*24
    delata_time =  delata_time/total_sec
    return 1/(1+delata_time)


def cal_item_slim(user_click,user_click_time):
    co_appear = {}
    item_user_click_item = {}
    for user,itemlist in user_click.items():
        for index_i in range(0,len(itemlist)):
            itemid_i = itemlist[index_i]
            item_user_click_item.setdefault(itemid_i,0)
            item_user_click_item[itemid_i] += 1
            for index_j in range(index_i + 1,len(itemlist)):
                itemid_j = itemlist[index_j]
                if user + "_" +itemid_i not in user_click_time:
                    click_time_one = 0
                else:
                    click_time_one = user_click_time[user + "_" + itemid_i]

                if user + "_" +itemid_j not in user_click_time:
                    click_time_two = 0
                else:
                    click_time_two = user_click_time[user + "_" + itemid_j]



                co_appear.setdefault(itemid_i,{})
                co_appear[itemid_i].setDefault(itemid_j,0)
                co_appear[itemid_i][itemid_j] += update_two_contribute_score(len(itemlist))

                co_appear.setdefault(itemid_j,{})
                co_appear[itemid_j].setDefault(itemid_i,0)
                co_appear[itemid_j][itemid_i] += update_two_contribute_score(len(itemlist))

    item_slim_score = {}
    item_slim_score_stored = {}
    for itemid_i,relate_item in co_appear.items():
        for itemid_j,co_time in relate_item.items():
            slim_score = co_time/math.sqrt(item_user_click_item[itemid_i],item_user_click_item[itemid_j])
            item_slim_score.setdefault(itemid_i,{})
            item_slim_score[itemid_i].setDefault(itemid_j,0)
            item_slim_score[itemid_i][itemid_j] = slim_score

        for itemid in item_slim_score:
            item_slim_score_stored[itemid] = sorted(item_slim_score[itemid].iteritems(),key= \
                                                    operator.itemgetter(1),reverse=True)

        return item_slim_score


def cal_recom_result(slim_info,user_click):
    recent_click_num = 3
    topk = 5
    recome_info = {}
    for user in user_click:
        click_list =user_click[user]
        recome_info.setdefault(user,{})
        for itemid in click_list[:recent_click_num]:
            if itemid not in slim_info:
                continue
            for itemslimzuhe in slim_info[itemid][:topk]:
                itemsmid = itemslimzuhe[0]
                itemsimscore = itemslimzuhe[1]
                recome_info[user][itemsmid] = itemsimscore
        return recome_info

def debugitemslim(item_info,slim_info):

    fixed_itemid = "1"
    if fixed_itemid not in item_info:
        print("invalid itemid")
        return
    [title_fix,genres_fix] = item_info[fixed_itemid]
    for zuhe in slim_info[fixed_itemid][:5]:
        itemid_slim = zuhe[0]
        sim_score = zuhe[1]
        if itemid_slim not in item_info:
            continue
        [title,genres] = item_info[itemid_slim]
        print (title_fix + "\t" +genres_fix +"\tsim:" +title +genres +"\t" +str(sim_score))

#推荐结果的debug
def debug_recomresult(recom_result,item_info):

    user_id = "1"
    if user_id not in recom_result:
        print("invalid result")
        return
    for zuhe in sorted(recom_result[user_id].iteritems(),key=operator.itemgetter("1"),reverse=True):
        itemid,score = zuhe
        if itemid not in item_info:
            continue
        print(",".join(item_info[itemid]) + "\t" +str(score))



def main_flow():
    user_click,user_click_time = reader.get_user_click("../Data/ratings.txt")
    item_info = reader.get_item_info("../Data/movies.txt")
    slim_info = cal_item_slim(user_click,user_click_time)
    debugitemslim(item_info,slim_info)
    recom_result = cal_recom_result(slim_info,user_click)




if __name__ == '__main__':
    main_flow()


