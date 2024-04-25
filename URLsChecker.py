# Import needed libraries
import argparse
import asyncio
import aiohttp
import sys
import os
from timeit import default_timer as timer


start = timer()
headers = {  # To fake a normal browser
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}


async def check_url(session, url, verbose):
    url = url.strip()
    if not url:
        return ''
    result = f"Invalid\t=> {url}"
    for protocol in ('https://', 'http://'):
        try:
            url_with_protocol = url if url.startswith(
                'http') else protocol + url
            async with session.get(url_with_protocol) as r:
                result = f"{r.status}\t=> {url_with_protocol}"
                break
        except Exception as e:
            # print(e)
            continue
    if verbose:
        print(result)
    return result


async def check_urls(session, urls, verbose):
    urls_count = len(urls)
    tasks = []
    for i, url in enumerate(urls, 1):
        task = asyncio.create_task(check_url(session, url, verbose))
        tasks.append(task)

        # Print the counter for every 10 requests when verbose is False
        if not verbose:
            print(f'==> Checked {i}/{urls_count} URLs <==', end='\r')

    results = await asyncio.gather(*tasks)
    return results


async def main(headers, urls, verbose):
    timeout = aiohttp.ClientTimeout(total=10)  # setting a timeout in seconds
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        data = await check_urls(session, urls, verbose)
        return data


def checkFiles(outputFile):
    # Save working urls [200 status code]
    valid = os.path.splitext(outputFile)
    validPath = valid[0]+'_Valid'+valid[1]
    # Save unvalid urls [not 200 status code]
    others = os.path.splitext(outputFile)
    otherPath = others[0]+'_Others'+others[1]

    # Check output files existance
    if os.path.isfile(validPath) or os.path.isfile(otherPath):
        print("Try again with a non-existing and valid output file name.")
        return False
    else:
        return True


def saveData(fullPath, data):
    fileName = os.path.splitext(fullPath)  # Split filename & extension
    fileName, fileExtension = os.path.splitext(fullPath)
    directory = f"{fileName}_Results"
    os.makedirs(directory, exist_ok=True)  # Create if doesn't exist

    # To save working urls
    validUrlsPath = os.path.join(directory, f"{fileName}_Valid{fileExtension}")
    # Save unvalid urls
    otherUrlsPath = os.path.join(
        directory, f"{fileName}_Others{fileExtension}")
    # Save forbidden urls
    forbiddenUrlsPath = os.path.join(
        directory, f"{fileName}_Forbidden{fileExtension}")

    with open(validUrlsPath, 'a') as validFile, \
            open(otherUrlsPath, 'a') as othersFile, \
            open(forbiddenUrlsPath, 'a') as forbiddenFile:
        for line in data:
            splitted = line.split("\t=> ")[0]
            status_code = None

            if len(splitted) > 0 and splitted.strip().isdigit():
                status_code = int(splitted)

            if status_code and 200 <= status_code < 300:  # Check for all 2xx status codes
                validFile.write(line + '\n')
            elif status_code and status_code == 403:  # Check for all 403 status codes
                forbiddenFile.write(line + '\n')
            else:
                othersFile.write(line + '\n')


def handleParsing():
    # parse all args
    parser = argparse.ArgumentParser(
        description='# A fast and easy-to-use tool to check and extract working URLs from a list of URLs.',
        epilog='test')
    parser.add_argument('-u', '--urls', type=argparse.FileType('r'), default=sys.stdin, required=True, dest='URLs_File', nargs=1,
                        help='choose your URLs file name')
    parser.add_argument('-o', '--output', type=str, default=sys.stdout, required=True, dest='Output_File', nargs=1,
                        help='choose the output file name')
    parser.add_argument('-sep', '--separator', type=str, default='\n', dest='URLs_Separator', nargs=1,
                        help=r'default=newline [\n]')
    parser.add_argument('-v', '--verbose',
                        action='store_true', help='print results in real-time')

    args = parser.parse_args()
    separator = args.URLs_Separator[0]
    output_file = args.Output_File[0]
    input_file = args.URLs_File[0].name

    filesExist = checkFiles(output_file)

    if (type(filesExist) == bool and filesExist == True):
        # import a file of urls
        with open(input_file) as urls_file:
            data = urls_file.read()

            # Replace separator string with actual character
            if '\\t' in separator:
                separator = separator.replace('\\t', '\t')
            elif '\\n' in separator:
                separator = separator.replace('\\n', '\n')
            # Split the data [str -> list]
            urls = data.split(separator)

        return {"urls": urls, "output_file": output_file, "verbose": args.verbose}
    else:
        return False


if __name__ == '__main__':
    data = handleParsing()

    if data:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())
        results = asyncio.run(main(headers, data['urls'], data['verbose']))

        saveData(data['output_file'], results)

        end = timer()
        print(f"Elapsed time: {end - start} seconds\n")
