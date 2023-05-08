from ShippingCost.pipeline import training_pipeline

if __name__== "__main__":
    try:
        training_pipeline.start_pipeline()
           
    except Exception as e:
        print(e)          