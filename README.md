# Simple Sports Data Analyzer

Analyze the crawled sports data.

## Table Description

### game_judgement

Record gambling result.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :---: |
| game_id | string | Game unique id, which comes from date(YYYYmmDD) + game id of that date. | 20190526496 |
| host_win_original | 0 or 1 | The host won the game originally. | 1 |
| host_win_point_spread_national | 0 or 1 | The host won the game with point spread gambling on national banker. | 1 |
| host_win_point_spread_local | 0 or 1 | The host won the game with point spread gambling on Taiwan banker. | 1 |
| over_total_point_national | 0 or 1 | The total score was over the threshold with total score gambling on national banker. | 1 |
| over_total_point_local | 0 or 1 | The total score was over the threshold with total score gambling on Taiwan banker. | 1 |

### prediction_judgement

Record judgements of predictions from members, those members been classified into 4 groups also, 
* all member: all members.
* all_prefer: all member with highly confident.
* more_than_sixty: members with more 60% hit ratio.
* top_100: top 100 members.

If the result of the majority members' prediction matching the actual game result, denote as 1 and vise versa.
 
For example: if there are 51% of group members voted that host will win the point spread gambling 
and the prediction was correct, denote the judgement result as 1.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :---: |
| game_id | string | Game unique id, which comes from date(YYYYmmDD) + game id of that date. | 20190526496 |
| national_point_spread_result | 0 or 1 | The prediction of the group member was correct with point spread gambling on national banker. | 1 |
| national_point_spread_percentage | int | Percentage of win members of the group in point spread gambling with national banker. | 51 |
| national_point_spread_population | int | Population of win members of the group in point spread gambling with national banker. | 935 |
| national_total_point_result | 0 or 1 | The prediction of the group member was correct with total score gambling on national banker. | 0 |
| national_total_point_percentage | int | Percentage of win members of the group in total score gambling with national banker. | 45 |
| national_total_point_population | int | Population of win members of the group in total score gambling with national banker. | 436 |
| local_point_spread_result | 0 or 1 | The prediction of the group member was correct with point spread gambling on local banker. | 1 |
| local_point_spread_percentage | int | Percentage of win members of the group in point spread gambling with local banker. | 55 |
| local_point_spread_population | int | Population of win members of the group in point spread gambling with local banker. | 919 |
| local_total_point_result | 0 or 1 | The prediction of the group member was correct with total score gambling on local banker. | 0 |
| local_total_point_percentage | int | Percentage of win members of the group in total score gambling with local banker. | 44 |
| local_total_point_population | int | Population of win members of the group in total score gambling with local banker. | 411 |
| local_original_result | 0 or 1 | The prediction of the group member was correct with original score gambling on local banker. | 1 |
| local_original_percentage | int | Percentage of win members of the group in original score gambling with local banker. | 82 |
| local_original_population | int | Population of win members of the group in original score gambling with local banker. | 451 |