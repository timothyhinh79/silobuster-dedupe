from tld import get_tld # to get domain extension (aka top-level domain or 'TLD') of URL
import random
from manglers.mangle_org_name import random_remove, random_replace, random_null
from manglers.tld_swap_probability_matrix import tld_swap_prob_matrix

# consider getting more extensive list of domain extensions, from data or from TLD website
domain_extensions = ['com', 'org', 'net', 'gov', 'edu', 'us']

# randomly remove www. from URL 
def remove_www(url, prob):
    random_value = random.random()
    mangled_url = url
    if random_value < prob:
        mangled_url = url.replace('www.', '')  
    return mangled_url

# randomly remove scheme from URL
def remove_scheme(url, prob):
    random_value = random.random()
    mangled_url = url
    if random_value < prob:
        mangled_url = url.replace('http://', '').replace('https://','')
    return mangled_url

# randomly remove s from https in URL
def remove_s_from_https(url, prob):
    random_value = random.random()
    mangled_url = url
    if random_value < prob and 'https://' in url:
        mangled_url = url.replace('https://', 'http://')
    return mangled_url

# randomly append extra forward slash (/) to end of URL if it does not already end with one
def append_extra_slash(url, prob):
    random_value = random.random()
    mangled_url = url
    if url and random_value < prob and url[-1] != '/':
        mangled_url = url + '/'
    return mangled_url


# randomly remove/replace characters in URL, and randomly set entire URL to NULL with given probabilities
def mispell_url(url, remove_prob, replace_prob, null_prob):
    mangled_url = random_null(url, null_prob)
    mangled_url = random_remove(url, remove_prob)
    mangled_url = random_replace(url, replace_prob)

    return mangled_url

def change_domain_extension(url, tld_swap_prob_matrix):
    try:
        tld = get_tld(url)
        random_tld = select_random_tld(tld_swap_prob_matrix[tld])
        mangled_url = url.replace('.' + tld, '.' + random_tld)
        return mangled_url
    except:
        return url  

def select_random_tld(prob_dict):
    prob_ranges = construct_prob_ranges(prob_dict)
    random_value = random.random()
    random_tld = [tld for tld, min_prob, max_prob in prob_ranges if random_value >= min_prob and random_value < max_prob]
    return random_tld[0]

def construct_prob_ranges(prob_dict):
    prob_ranges = []
    prob_val = 0
    for tld, tld_prob in prob_dict.items():
        prob_ranges.append((tld, prob_val, prob_val + tld_prob))
        prob_val += tld_prob
    
    return prob_ranges

def mangle_url(url, probs_dict, tld_swap_prob_matrix):

    mangled_url = change_domain_extension(url, tld_swap_prob_matrix) # swapping TLD first to minimize chances of creating bad URL before trying to identify the TLD..
    mangled_url = remove_www(mangled_url, probs_dict['www_remove_prob'])
    mangled_url = remove_scheme(mangled_url, probs_dict['scheme_remove_prob'])
    mangled_url = remove_s_from_https(mangled_url, probs_dict['remove_s_from_https_prob'])
    mangled_url = append_extra_slash(mangled_url, probs_dict['append_extra_slash_prob'])
    mangled_url = mispell_url(mangled_url, probs_dict['mispell_remove_char_prob'], probs_dict['mispell_replace_char_prob'], probs_dict['mispell_null_url_prob'])

    return mangled_url

