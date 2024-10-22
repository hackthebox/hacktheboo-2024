<img src="../../assets/banner.png" style="zoom: 80%;" align=center />

<img src="../../assets/logo.png" style="zoom: 80%;" align='left' /><font size="6">LinkHands</font>

  1<sup>st</sup> 10 24 / Document No. D24.102.167

  Prepared By: clubby789

  Challenge Author: clubby789

  Difficulty: <font color=green>Easy</font>

  Classification: Official






# Synopsis

LinkHands is an Easy reversing challenge. Players must identify two linked lists of global variables, and re-link them to gain the flag. 

## Skills Required
    - Use of a decompiler
## Skills Learned
    - Linked list datastructure basics

# Solution

Running the binary, we're given this message:

```
The cultists look expectantly to you - who will you link hands with?
```
Entering random input results in failure:
```
You fail to grasp their hands - they look at you with suspicious...
```

## Analysis

We'll decompile the binary.

```c
printf(format: "The cultists look expectantly to you - who will you link han…")
char buf[0x40]
fgets(&buf, n: 0x40, fp: stdin)
char* newline = strchr(&buf, 0xa)

if (newline != 0)
    *newline = 0

void* ptr1
void* ptr2
int32_t result

if (__isoc99_sscanf(s: &buf, format: "%p %p", &ptr1, &ptr2) != 2) {
    puts(str: "You fail to grasp their hands - they look at you with suspic…")
    result = 1
} else {
    *ptr1 = ptr2
    
    for (void* i = &data_404190; i != 0; i = *i)
        putchar(c: *(i + 8))
    
    putc(c: 0xa, fp: stdout)
    result = 0
}
```

It expects two pointers as input - one is used to assign to the other. We then iterate over some global variable, printing out characters - this can be identified as a linked list if we add a type:

```c
struct ListNode {
    struct ListNode* next;
    char c;
}
```

```c
    left->next = right
    
    for (struct ListNode* cur = &head; cur != 0; cur = cur->next)
        putchar(c: cur->c)
    
    putc(c: '\n', fp: stdout)
    result = 0

```

If we look at the global variable, we can see a chain of nodes:

```c
struct ListNode head = 
{
    struct ListNode* next = data_4041a0
    char c = 'H'
                                                                           00 00 00 00 00 00 00                           .......
}
struct ListNode data_4041a0 = 
{
    struct ListNode* next = data_4041b0
    char c = 'T'
                           00 00 00 00 00 00 00                                                           .......
}
struct ListNode data_4041b0 = 
{
    struct ListNode* next = data_4041c0
    char c = 'B'
                                                                           00 00 00 00 00 00 00                           .......
}
struct ListNode data_4041c0 = 
{
    struct ListNode* next = 0x4041d0
    char c = '{'
                           00 00 00 00 00 00 00                                                           .......
```

It seems to be the start of a flag. However, the chain ends with a `_` character which has a `next` field of `NULL`.

Immediately after this entry are what appear to be several more entries - they form their own chain, starting with `c` and ending with `}`.

We must therefore provide the address of the *last* entry in the first chain and the *first* entry of the second, linking them together. In this case, the addresses are `0x404060` and `0x404070`. If we enter these two addresses, the whole flag is iterated over and printed.