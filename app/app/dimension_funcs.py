import re, math
from fractions import Fraction

def cln_dec(dec_num, dec_len=4):
    cln_num = ("{:." + str(dec_len) + "f}").format(dec_num).rstrip('0').rstrip('.')
    return(cln_num)

def convert_ft_in_to_feet(mixed_string):

    def eval_simple_fraction(simple_fraction_string):
        split_fraction = simple_fraction_string.split('/')
        numerator = int(split_fraction[0])
        denominator = int(split_fraction[1])
        return numerator / denominator

    def eval_mixed_number(mixed_number_string):
        split_number = mixed_number_string.split()
        whole_number = split_number[0]
        simple_fraction = split_number[1]
        fraction_value = eval_simple_fraction(simple_fraction)
        return int(whole_number) + fraction_value

    def process_inches(inch_string):
        try:
            inch_num = float(inch_string)
            return inch_num
        except:
            if re.search("^(\d+(?:(?: \d+)*\/\d+)?)$", inch_string):
                try:
                    inch_num = eval_simple_fraction(inch_string)
                    return inch_num
                except:
                    inch_num = eval_mixed_number(inch_string)
                    return inch_num
            else:
                raise ValueError('not a valid number')

    try:
        split_string = mixed_string.split('-')
        foot_string = split_string[0].replace('\'', '').strip()
        inch_string = split_string[1].replace('"', '').strip()
        inches = process_inches(inch_string)
        feet = float(foot_string) + inches / 12
        return feet
    except:
        raise ValueError('not a valid dimension')

def convert_feet_to_ft_in(feet_decimal, multiple=1/16/12, direction='nearest'):

    def round_number(raw_num, multiple, direction='nearest'):
        tolerance = multiple / 2
        fixed_num = (raw_num / tolerance) * tolerance
        if direction == 'up':
            rnd_num = multiple * math.ceil(fixed_num / multiple)
        elif direction == 'down':
            rnd_num = multiple * math.floor(fixed_num / multiple)
        else:
            rnd_num = multiple * round(fixed_num / multiple)
        return rnd_num

    def convert_decimal_to_mixed_number(decimal_num, multiple):
        whole_num = int(decimal_num)
        fraction = Fraction(decimal_num % 1).limit_denominator(int(1/multiple))
        mixed_number = str(whole_num) + ' ' + str(fraction)
        return mixed_number

    rnd_num = round_number(feet_decimal, multiple, direction)
    feet = int(rnd_num)
    inches = (rnd_num - feet) * 12
    inch_string = convert_decimal_to_mixed_number(inches, multiple)
    mixed_string = str(feet) + '\'-' + inch_string + '"'
    return mixed_string
