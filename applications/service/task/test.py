#调用mj服务""


all_tags = [{"id": 1, "tag_name": "tag1", "parent_id": 0},
            {"id": 2, "tag_name": "tag2", "parent_id": 1},
            {"id": 3, "tag_name": "tag3", "parent_id": 1},
            {"id": 4, "tag_name": "tag4", "parent_id": 2},
            {"id": 5, "tag_name": "tag5", "parent_id": 2},
            {"id": 6, "tag_name": "tag6", "parent_id": 2},
            {"id": 7, "tag_name": "tag7", "parent_id": 3},
            {"id": 8, "tag_name": "tag8", "parent_id": 3},
            {"id": 9, "tag_name": "tag9", "parent_id": 3},
            {"id": 10, "tag_name": "tag10", "parent_id": 3}
        ]
second_tags = []
third_tag = []
for tag in all_tags:
    if tag.get("parent_id") == 1:
        second_tags.append(tag)
print(len(second_tags))
print(second_tags)
for j in range(len(second_tags)):
    id = second_tags[j].get("id")
    tag_name = []
    for t in all_tags:
        if id == t.get("parent_id"):
            tag_name.append(t.get("tag_name"))
    print(tag_name)
    third_tag.append(tag_name)
print(third_tag)
