channels = ['IL', 'KT', 'SD', 'SV1D', 'SV2C', 'SV1B', 'IDA', 'QD', 'AM', 'SB2B',
'MCP', 'KB', 'RV', 'QE', 'VN', 'SV1C', 'SV2B', 'SV2D', 'IH', 'BC', 'PR',
'VP', 'RSE', 'IDQ', 'VU', 'SV3B', 'MCR', 'RSD', 'KTI', 'QS', 'SV1A',
'TT', 'IDE', 'IDS', 'SV', 'SV2A', 'SV3C', 'CC', 'TE', 'RIE', 'ROE',
'SV3E', 'SV3A', 'RCM', 'DC', 'KTC', 'RB']

def get_channels():
    new_channels = set()
    for channel in channels:
        new_channels.add(channel + "_Tutor")
        new_channels.add(channel + "_Tutee")
    return new_channels
