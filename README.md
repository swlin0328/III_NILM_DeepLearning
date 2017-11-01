# III_PowerNILM_DeepLearning
III_PowerNILM_DeepLearning is a module for estimating the energy consumed by individual appliances from aggregate consumption data. In this project, unlike REDD or UKDALE, the sample rate of III's power data is 60/sec or 180/sec.

Now, we are at THE VERY BEGINNING. One of our big challanges is to estimate the consumption of air conditioner from aggregate consumption, because electric behavior of air conditioners(AC) vary with brand, environmental temperature and size.

# Data Management  
We take REDD dataset as reference, which can be found in the below link:

http://redd.csail.mit.edu/

Then, we use Convert_TaiPower.py to convert our data to HDF formet. Here is the brief summary:
-Raw Data ---III.py or PongHu.py---> REDD format ---Convert_TaiPower.py---> HDF format ---> NILMTK

# From SQL to REDD format
-./III.py :  III's domestic
-./III.py -c :  III's commerce
-./ PongHu.py : 澎湖低碳島

# From REDD format to HDF
-./Convert_TaiPower.py

# Python note
We use pandas==0.16.2 instead of 0.19.2 . Though pandas==0.19.2 is better in resampling, neuralnilm is based on pandas==0.16.2. There is a bug when using pandas==0.19.2
