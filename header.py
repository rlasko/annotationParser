channels = ['RSE', 'N', 'MCR', 'AM', 'VP', 'SV1C', 'SV1B', 'PR', 'TT', 'SV3B',
'CC', 'SV2B', 'QE', 'QS', 'RV', 'gP', 'IDS', 'SV2D', 'gE', 'KTC', 'IDE', 'RB',
'SVA1', 'gN', 'VN', 'SV3E', 'SV3C', 'RNSD', 'gO', 'VU', 'TE', 'KT', 'SV', 'IH',
'BC', 'RCM', 'IDA', 'SB2B', 'SV2A', 'IL', 'SV1D', 'KTI', 'SV2C', 'RBC', 'KB',
'DC', 'IDQ', 'QD', 'SV3A', 'SD', 'RSD', 'MCP', 'SV1A']

def get_channels():
    new_channels = []
    for channel in channels:
        new_channels.append(channel + "_Tutor")
        new_channels.append(channel + "_Tutee")
    return sorted(new_channels)
