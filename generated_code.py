from diffusers import DDPMPipeline

model_id = "google/ddpm-cat-256"
ddpm = DDPMPipeline.from_pretrained(model_id)
image = ddpm().images[0]
image.save("ddpm_generated_cat_image.png")
