list_of_feed_p3_p4 = [
    0.038,
    0.045,
    0.051,
    0.057,
    0.064,
    0.070,
    0.077,
    0.083,
    0.089,
    0.096,
    0.10,
]

multiplier_p3_p4_to_m2 = 0.5
multiplier_p3_p4_to_n2_n3_n4 = 2


def transform_feeds(list_of_feed, multiplier):
    new_feed_list = [f * multiplier for f in list_of_feed]
    print()
    for feed in new_feed_list:
        print(feed)
    print()

if __name__ == '__main__':
    transform_feeds(list_of_feed=list_of_feed_p3_p4, multiplier=multiplier_p3_p4_to_m2)
    transform_feeds(list_of_feed=list_of_feed_p3_p4, multiplier=multiplier_p3_p4_to_n2_n3_n4)
