from execute import VkFunction

vk_get_25req_messages = VkFunction(args=("peer_id", "offset"), clean_args=("peer_id", "offset"), code="""
var params = {"peer_id": %(peer_id)s, "offset": %(offset)s, "count": 200};
var i = 0;
var items = [];
while (i<25) {
    var result = API.messages.getHistory(params);
    if (result.items.length == 0) {
        i = 25;
    } else {
        items = items + result.items;
        params.offset = params.offset + 200;
        i = i + 1;
    }
};
return items;
""")
