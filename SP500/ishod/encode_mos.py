# # -*- coding: utf-8 -*-
# import Crypto
# from Crypto.PublicKey import RSA
# from Crypto.Signature import pkcs1_15
# from Crypto import Random
# from Crypto.Hash import SHA256
# from Crypto.Cipher import PKCS1_OAEP
# # from hashlib import sha256
# #
import hashlib

# hashlib module is a popular module to do hashing in python

# Constructors of md5(), sha1(), sha224(), sha256(), sha384(), and sha512() present in hashlib
md = hashlib.md5()
my_account = "U3774281"  #"DU2079632" - demo  # "U3774281" - real
my_account = my_account[0::2] + my_account + my_account + my_account + my_account[0::3] + my_account[0::4]
print(my_account)
md.update(my_account.encode('utf-8'))
print(md.digest())
print("Digest Size:", md.digest_size, "\n", "Block Size: ", md.block_size)

# Comparing digest of SHA224, SHA256,SHA384,SHA512
my_str_enc = hashlib.sha224(my_account.encode('utf-8')).hexdigest()

######################################
# этои числа и есть шифрованный аккаунт - копируем в mos.json
print(my_str_enc)
print("Digest SHA224", hashlib.sha224(my_account.encode('utf-8')).hexdigest())


######################################
# print ("Digest SHA256", hashlib.sha256(my_account.encode('utf-8')).hexdigest())
# print ("Digest SHA384", hashlib.sha384(my_account.encode('utf-8')).hexdigest())
# print ("Digest SHA512", hashlib.sha512(my_account.encode('utf-8')).hexdigest())

# ----------------------------------------
# # проценты
# mp=hashlib.md5()
# my_proc = "1"
# mp.update(my_proc.encode('utf-8'))
# print (mp.digest())
# print ("Digest Size:", mp.digest_size, "\n", "Block Size: ", mp.block_size)
#
# # Comparing digest of SHA224, SHA256,SHA384,SHA512
# my_proc_enc = hashlib.sha256(my_proc.encode('utf-8').hexdigest())
# print(my_proc_enc)
# print ("Digest SHA224", hashlib.sha224(my_proc.encode('utf-8')).hexdigest())
# print ("Digest SHA256", hashlib.sha256(my_proc.encode('utf-8')).hexdigest())
# print ("Digest SHA384", hashlib.sha384(my_proc.encode('utf-8')).hexdigest())
# print ("Digest SHA512", hashlib.sha512(my_proc.encode('utf-8')).hexdigest())
#
#


def resvalacc(acc=""):
    md = hashlib.md5()
    my_str = acc  # "DU2079632_1"
    my_str = my_str[0::2] + my_str + my_str + my_str + my_str[0::3] + my_str[0::4]
    # my_account = my_account[0::2] + my_account + my_account + my_account + my_account[0::3] + my_account[0::4]
    print(my_str)
    md.update(my_str.encode('utf-8'))
    print(md.digest())
    print("Digest Size:", md.digest_size, "\n", "Block Size: ", md.block_size)

    # Comparing digest of SHA224, SHA256,SHA384,SHA512
    my_str_enc = hashlib.sha224(my_str.encode('utf-8')).hexdigest()
    print(my_str_enc)
    print("Digest SHA224", hashlib.sha224(my_str.encode('utf-8')).hexdigest())
    # print ("Digest SHA256", hashlib.sha256(my_account.encode('utf-8')).hexdigest())
    # print ("Digest SHA384", hashlib.sha384(my_account.encode('utf-8')).hexdigest())
    # print ("Digest SHA512", hashlib.sha512(my_account.encode('utf-8')).hexdigest())
    return my_str_enc

# -----------------------------------------------------------
#
# def generate_key():
#     KEY_LENGTH = 1024
#     # random_value = text   #
#
#     random_value2 =  5 -> bytes:...  #(5).to_bytes(10, byteorder='big')  #bytes(3)    #'123123'.encode('utf-8') # bytes(3.)
#     Random.new().read
#     # print(f'rand: {random_value}')
#     print(f'rand2: {random_value2}')
#     keyPair=RSA.generate(KEY_LENGTH,random_value2)
#     # keyPair.d. = 3888775389336691482834489880428088266761365835249111941727913582216300583545935245157829859526916730841536939001419809141523906622379269008987427879321370021591905189757553350166781531185277092771584528816129758917849275306462745448839896586600090356610234635804373909753385047924648636370358543989453386913
#     # keyPair.e = 65537
#     # keyPair.n = 133620415601691060666125810884454187734396871414568882903716675517848492490658838602888166115247575212772705192940955976079020762833381764964352880597912270902909004506285835567924964556395070862309010409013760831944106988694883363945417404429210011419174183571049192099817285940211316753900361308746434645633
#     # keyPair.p = 10592436060434448271649348533328777756777188236007720647549122511341292466296355924976315523653268652271807637716460191187687542075285504444404347676996861
#     # keyPair.q = 12614701173491022757604413361736553260522220738435709735437558180081642377423157150430946956130065325329802535250758374300339786841425506618810670966692053
#     # keyPair.u = 230951441033369782778669093625799812718228185678045258756795303820967933348761874274427892180325026461120531795298170977680919621272707246955907103845599
#
#     return keyPair
#
# # генерация ключей для Алисы и Боба
# bobKey=generate_key()
# # aliceKey=generate_key()
# print('1:', bobKey)
# # print('2:', aliceKey)
#
# # публичные ключи для Алисы и Боба
# # alicePK=aliceKey.publickey()
# bobPK=bobKey.publickey()
#
# # print ("Alice's Public Key:", alicePK)
# print ("Bob's Public Key:", bobPK)
#
# secret_message="Alice's secret message to Bob 111"
# print ("Message to Bob:", secret_message)
#
# # Зашифруем сообщение открытым ключем Боба - определяем адресата
# cipher = PKCS1_OAEP.new(bobPK)
# encrypted_for_bob = cipher.encrypt(secret_message.encode('utf-8'))
# print("encrypted_for_bob:", encrypted_for_bob)
# # Боб расшифровывает сообщение с помощью своего приватного ключа
# cipher = PKCS1_OAEP.new(bobKey)
# decrypted_message = str((cipher.decrypt(encrypted_for_bob)),'utf-8')
# print ("Decrypted message:", decrypted_message)
#
