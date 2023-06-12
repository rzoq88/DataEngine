import hashlib
def generate_unique_id(url):
    # Create a hashlib object using SHA256 algorithm
    hasher = hashlib.sha256()

    # Convert the text to bytes and update the hasher
    hasher.update(url.encode('utf-8'))

    # Get the hexadecimal representation of the hash value
    unique_id = hasher.hexdigest()

    return unique_id

def generate_unique_url(url):
    # Create a hashlib object using SHA256 algorithm
    hasher = hashlib.sha1

    # Convert the text to bytes and update the hasher
    hasher.update(url.encode('utf-8'))

    # Get the hexadecimal representation of the hash value
    unique_id = hasher.hexdigest()

    return unique_id