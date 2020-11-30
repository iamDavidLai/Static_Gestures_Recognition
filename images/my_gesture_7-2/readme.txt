test\
train\
validation\

	class_0_none
	class_1_fist
	class_2_iloveyou
	class_3_five
	class_4_okay
	class_5_peace
	class_6_straight
	class_7_thumbs
	
	
The image in these folders is for reference.
You can use gesture_getBinary.py to capture the gesture pics youn want.


Using Data Augmentation, 
In Keras, the ImageDataGenerator class has flow_from_directory()  to read images.
Please note the naming rule of folder.
The folder names for classes(labels) are very important!

class_"label"_"the name you want"  ==   class_0_none







