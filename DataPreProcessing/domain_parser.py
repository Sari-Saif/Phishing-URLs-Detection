import tldextract
import re

def parse(domain_list, class_info, count):
    parsed_domain_list = []
    registered_domain_lst = []

    for line in domain_list:
        domain = {}
        line = line.strip().replace('"', "").replace("'",'')
        extracted_domain = tldextract.extract(line)

        registered_domain_lst.append(extracted_domain.registered_domain)

        domain['url'] = line
        domain['domain'] = extracted_domain.domain
        domain['registered_domain'] = extracted_domain.registered_domain
        domain['tld'] = extracted_domain.suffix
        domain['subdomain'] = extracted_domain.subdomain
        domain['class'] = class_info
        domain['id'] = count
        count = count + 1

        if line.find('://') == -1:
            domain['protocol'] = ''
        else:
            domain['protocol'] = line.split("://")[0]

        tmp = line[line.find(extracted_domain.suffix):len(line)]
        pth = tmp.partition("/")
        domain['path'] = pth[1] + pth[2]

        domain['words_raw'] = words_raw_extraction(extracted_domain.domain, extracted_domain.subdomain, pth[2])

        parsed_domain_list.append(domain)

    return parsed_domain_list

def parse_nonlabeled_samples(domain_list, count=0):
    parsed_domain_list = []
    registered_domain_lst = []

    for line in domain_list:
        domain = {}

        extracted_domain = tldextract.extract(line)

        registered_domain_lst.append(extracted_domain.registered_domain)

        domain['url'] = line.strip()
        domain['domain'] = extracted_domain.domain
        domain['registered_domain'] = extracted_domain.registered_domain
        domain['tld'] = extracted_domain.suffix
        domain['subdomain'] = extracted_domain.subdomain
        domain['id'] = count
        count = count + 1

        if line.find('://') == -1:
            domain['protocol'] = ''
        else:
            domain['protocol'] = line.split("://")[0]

        tmp = line[line.find(extracted_domain.suffix):len(line)]
        pth = tmp.partition("/")
        domain['path'] = pth[1] + pth[2]

        domain['words_raw'] = words_raw_extraction(extracted_domain.domain, extracted_domain.subdomain, pth[2])

        parsed_domain_list.append(domain)

    return parsed_domain_list

def words_raw_extraction(domain, subdomain, path):

    w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
    w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())
    w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())

    raw_words = w_domain + w_path + w_subdomain
    raw_words = list(filter(None, raw_words))

    return raw_words
