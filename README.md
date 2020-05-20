# TD-W8950N
![web](https://i.imgur.com/2DK1Py1.jpg)

Firmware Version: 	1.0.2 Build 150205 Rel.66189

Hardware Version: 	TD-W8950N V1 0x00000001

```python
router = Router('admin', 'admin') # login, pass
users = router.users() # MAC
router.add_mac_filter(users[0])
router.delete_mac_filter(users[0])
router.set_mac_filter_mode('disabled') # 'disabled', 'allow', 'deny'
router.set_password('admin', 'ADMIN') # 'admin', 'user'
print(router.get_password())
router.reboot()
```
