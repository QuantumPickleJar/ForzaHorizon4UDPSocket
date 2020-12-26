# Write your code here :-)
import socket
import logging
import datetime as dt

from fdp import ForzaDataPacket

rpm = None

def to_str(value):
    '''
    Returns a string representation of the given value, if it's a floating
    number, format it.

    :param value: the value to format
    '''
    if isinstance(value, float):
        return('{:f}'.format(value))

    return('{}'.format(value))

def main():

    config = None
    # fetch the config params
    import yaml
    # with open('/home/pi/Desktop/forza_motorsport-master/config.yaml') as f:
    with open('D:/Python/Forza/ForzaUDPSoccket/ForzaUDPSoccket/forza/config.yaml') as f:
        try:
            config = yaml.safe_load(f)
            print(config)
        except yaml.YAMLError as exc:
            print('error!')
            print(exc)
    if config:
        # The configuration can override everything
        if 'port' in config:
            port = config['port']
            print('assigned port to ',port)

        if 'format' in config:
            format = config['format']

        if 'append' in config:
            append = config['append']

        if 'packet_format' in config:
            packet_format = config['packet_format']

    params = ForzaDataPacket.get_props(packet_format=packet_format)
    if config and 'parameter_list' in config:
        params = config['parameter_list']

    log_wall_clock = False
    if 'wall_clock' in params:
        log_wall_clock = True

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))


    print('listening on port {}'.format(port))
    n_packets = 0

    while True:
        # print('while true!')
        message, address = server_socket.recvfrom(1024)
        fdp = ForzaDataPacket(message, packet_format = packet_format)
        if log_wall_clock:
                fdp.wall_clock = dt.datetime.now()


        if n_packets == 0:
            print('{}: logging data')
            print('\t'.join(params))
        else:
            for index, val in enumerate(fdp.to_list(params)):
                print(params[index],val)
                #logging.info(params[index],val)

        n_packets += 1
        if n_packets % 60 == 0:
            print('{}: logged {} packets'.format(dt.datetime.now(), n_packets))


if __name__ == "__main__":
    main()