import fiftyone.zoo as foz
dataset=foz.load_zoo_dataset("open-images-v6",split="validation",
                                      label_types=['detections'], classes=["Person", "Man", "Woman"], 
                                      max_samples=800, seed=51, shuffle=True,)







                                      