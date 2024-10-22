<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">CryptOfTheUndead</font>

  9<sup>th</sup> 10 24 / Document No. D24.102.170

  Prepared By: clubby789

  Challenge Author: clubby789

  Difficulty: <font color=green>Very Easy</font>

  Classification: Official






# Synopsis

CryptOfTheUndead is a Very Easy reversing challenge. Players will reverse engineer a ransomware binary to uncover a static key, then decrypt a file to gain the flag.

## Skills Required
    - Decompiler usage
## Skills Learned
    - Recognizing cryptographic primitives
    - Bypassing program checks

# Solution

We're provided two files; `crypt` and `flag.txt.undead`. Running `crypt` gives us an error:

```
Usage: ./crypt file_to_encrypt
```
so we can surmise that this is possibly some kind of ransomware, used to encrypt files. `flag.txt.undead` seems to contain random bytes, so it is likely encrypted.

## Analysis

Opening it in a decompiler, we can see the program is not stripped.

```c
int32_t main(int32_t argc, char** argv, char** envp)
int32_t return

if (argc s<= 1) {
    char const* const program_name = "crypt"
    
    if (argc == 1)
        program_name = *argv
    
    return = 1
    printf(format: "Usage: %s file_to_encrypt\n", program_name)
```
We begin by checking the args, and printing a help string if used incorrectly.

We then check the file argument passed, and ensure it doesn't end with `.undead`:

```c
    char* old_filename = argv[1]
    
    if (ends_with(old_filename, ".undead") != 0) {
        return = 2
        puts(str: "error: that which is undead may not be encrypted")
```

We'll then allocate space for our new filename, likely used for the post-encryption fike, and append `.undead` to the old filename.

```c
    uint64_t new_filename_len = strlen(old_filename) + 9
    char* new_filename_buf = malloc(bytes: new_filename_len)
    strncpy(new_filename_buf, old_filename, new_filename_len)
    *(new_filename_buf + strlen(new_filename_buf)) = '.undead'
```

We then perform the encryption.
```c
    if (read_file(old_filename, &nbytes_1, &buf_1) != 0)
        return main.cold() __tailcall

    uint64_t nbytes = nbytes_1
    void* buf = buf_1
    encrypt_buf(buf, nbytes, "BRAAAAAAAAAAAAAAAAAAAAAAAAAINS!!")
    int32_t return_1 = rename(old: old_filename, new: new_filename_buf)
    return = return_1
```
`main.cold` is a short function that prints an error message then exits. If the read is successful, we call `encrypt_buf` on it. We then use `rename` to rename the file to the new name.

Looking into `encrypt_buf`:

```c
int64_t encrypt_buf(char* buf, uint64_t buflen, uint8_t* key)
uint8_t nonce[0xc]
nonce[0].q = 0
nonce[8].d = 0
struct chacha_ctx ctx
chacha20_init_context(&ctx, key, &nonce, 0)
chacha20_xor(&ctx, buf, buflen)
```
We can see it uses `chacha20` to encrypt a buffer with a given key and a nonce of 0. Even if this file was stripped, we could recognize this as `chacha20` by the cryptographic constant used in `chacha20_init_context`:

```c
__builtin_strncpy(dest: &arg1[0x10], src: "expand 32-byte k", n: 0x10)
```

## Decryption

Knowing the algorithm (chacha20) and the key (`BRAAAAAAAAAAAAAAAAAAAAAAAAAINS!!`) is enough to encrypt this file. However, we can use a useful property of chacha20 instead. It is a reversible stream cipher, meaning that the 'encrypt' operation can be re-run on ciphertext with the same key to produce the plaintext.

The binary prevents this by checking for the `.undead` suffix. However, we can either patch that check out, or simply rename `flag.txt.undead` to `flag.txt`. We then run the binary on `flag.txt`, and read `flag.txt.undead` to reveal the flag.
 