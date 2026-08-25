Yes, you can completely change how PyCharm handles Alt key combinations. By default, PyCharm interprets Alt as a command modifier or an action shortcut, which frequently collides with global system hotkeys or OS-level compose key sequences.
You can fix this inside PyCharm using two different methods: remapping the specific shortcut or disabling the Windows Alt menu behavior entirely inside the IDE.
## Method 1: Change the Extract Function Shortcut (Recommended)
If Alt combinations are blocked by your system, change the PyCharm shortcut to use a completely different modifier sequence (like Ctrl + Shift + X).

   1. Open PyCharm Settings using Ctrl + Alt + S.
   2. Select Keymap from the left-hand menu.
   3. In the search box, type Extract Method.
   4. Right-click Extract Method in the results list and select Add Keyboard Shortcut.
   5. Press your new desired sequence (for example: Ctrl + Shift + M or Ctrl + Shift + X).
   6. Click OK, then click Apply. [1, 2] 

## Method 2: Disable the Windows Alt Key Mnemonics
Windows often forces PyCharm to focus on the top window menu (File, Edit, View) whenever Alt is pressed, which completely breaks active shortcuts like Ctrl + Alt + M. You can turn this off:

   1. Open PyCharm Settings using Ctrl + Alt + S.
   2. Navigate to Appearance & Behavior > Appearance.
   3. Scroll down to the UI Options section.
   4. Uncheck the box next to Disable mnemonics in menu (or Support screen readers, which forces standard keyboard hooks).
   5. Alternatively, open Advanced Settings from the left menu, search for Alt, and ensure Disable mnemonics in menu is explicitly checked to prevent the Alt key from stealing focus from the editor. [3] 

## Method 3: Redefine the Global Keymap Scheme
If all Alt keys are causing issues across the board on your Lenovo machine, you can switch PyCharm to a non-conflicting keymap profile:

   1. Go to Settings > Keymap.
   2. Click the dropdown menu at the very top (it likely says Windows or Default).
   3. Change it to GNOME or Visual Studio.
   4. These alternative layouts drastically reduce the number of shortcuts reliant on the Alt key, moving critical functions to Ctrl and Shift variations instead. [4] 

Does changing the Extract Method shortcut to a Ctrl + Shift combination bypass the system conflict for you, or do you need help mapping a specific alternative key sequence?

[1] [https://tms-outsource.com](https://tms-outsource.com/blog/posts/pycharm-keyboard-shortcuts/)
[2] [https://www.youtube.com](https://www.youtube.com/watch?v=cCNJckoUTS0)
[3] [https://www.youtube.com](https://www.youtube.com/watch?v=6lspF_ohQIE)
[4] [https://www.geeksforgeeks.org](https://www.geeksforgeeks.org/python/how-to-customize-and-configure-pycharm/)

## https://www.jetbrains.com/help/pycharm/mastering-keyboard-shortcuts.html#ws_print_keymap

https://www.jetbrains.com/help/pycharm/configuring-keyboard-and-mouse-shortcuts.html#add-keyboard-shortcut