# Comparing-images
Structural similarity index (SSIM) and mean squared error (MSE)


SSIM is a method that attempts to model the perceived change in the structural information of the image (Wang et al., 2004). The SSIM can be interpreted as a measure of quality of one of the images that are compared, while the other image is considered of perfect quality. The index equation is as follows:

$$SSIM (x, y) = \frac {(2 \mu_x \mu_y + C_1) (2 \sigma_{xy} + C_2)} {(\mu_x^2 + \mu_y^2 + C_1) (\sigma_x^2 + \sigma_y^2 + C_2)}$$

where $\mu$ is the average of the intensities of the pixels in the x and y direction; $\sigma$ is the variance of the intensities in the x and y direction; and $\sigma_{xy}$ is the covariance. The value of SSIM varies between -1 and 1, where 1 indicates a perfect similarity.


<p align="center">
  <img width=285 src="2016_05_15_ETobserved.png"/>
  <img width=285 src="2016_05_15_ETmodeled.png"/>
  <img width=285 src="2016_05_15_ET_RMSE.png"/>
</p>




SSIM: 0.156 

RMSE: 0.389


Dependences:

    python - Scikit-image
    python - Pandas
    python - NumPy
    python - Matplolib
    python - Gdal
    python - Scikit-learn


Page source:

http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
