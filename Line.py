Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> class Line(object):
    	#"""
    	#Line: y = ax + b.
    	#A line can be described by its pair of coordinates (x1, y1), (x2, y2).
    	#To formalize a line, we need to compute its slope (a) and intercept (b).
    	#"""
    
    	def __init__(self, x1, y1, x2, y2):
        	if x1 > x2: (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
        	self.x1, self.y1 = x1, y1
        	self.x2, self.y2 = x2, y2
        	self.a = self.compute_slope()
        	self.b = self.compute_intercept()
        	self.lane_line = self.assign_to_lane_line()
        
        
    	def __repr__(self):
        	return 'Line: x1={}, y1={}, x2={}, y2={}, a={}, b={}, candidate={}, line={}'.format(
                	self.x1, self.y1, self.x2, self.y2, round(self.a,2), 
                	round(self.b,2), self.candidate, self.lane_line)
    
    	def get_coords(self):
        	return (self.x1, self.y1, self.x2, self.y2)

    	def get_x_coord(self, y):
        	return int((y - self.b) / self.a)
    
    	def get_y_coord(self, x):
        	return int(self.a * x + self.b)
    
    	def compute_slope(self):
        	return (self.y2 - self.y1) / (self.x2 - self.x1)
    
    	def compute_intercept(self):
        	return self.y1 - self.a * self.x1
    
    #property
    	def candidate(self):
        	#"""
        	#A simple domain logic to check whether this hough line can be a candidate 
        	#for being a segment of a lane line.
        	#1. The line cannot be horizontal and should have a reasonable slope.
        	#2. The difference between lane line's slope and this hough line's cannot be too high.
        	#3. The hough line should not be far from the lane line it belongs to.
        	#4. The hough line should be below the vanishing point.
        	#"""
        	if abs(self.a) < Lane.MOSTLY_HORIZONTAL_SLOPE: return False
        	lane_line = getattr(Lane, self.lane_line)
        	if lane_line:
            		if abs(self.a - lane_line.coeffs[0]) > Lane.MAX_SLOPE_DIFFERENCE: return False
            		if self.distance_to_lane_line > Lane.MAX_DISTANCE_FROM_LINE: return False
            		if self.y2 < Lane.left_line.vanishing_point[1]: return False
        	return True
    
    	def assign_to_lane_line(self):
        	if self.a < 0.0: return 'left_line'
        	else: return 'right_line'
        
    #property
    	def distance_to_lane_line(self):
        	#"""
        	#Reference https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        	#"""
        	lane_line = getattr(Lane, self.lane_line)
       	 	if lane_line is None: return None
        	avg_x = (self.x2 + self.x1) / 2
        	avg_y = (self.y2 + self.y1) / 2
        	distance = abs(lane_line.a * avg_x - avg_y + 
                   	lane_line.b) / math.sqrt(lane_line.a ** 2 + 1)
        	return distance

	def gimp_to_opencv_hsv(*hsv):
    	#"""
    	#I use GIMP to visualize colors. This is a simple
    	#GIMP => CV2 HSV format converter.
    	#"""
    		return (hsv[0] / 2, hsv[1] / 100 * 255, hsv[2] / 100 * 255)

	# A fixed polygon coordinates for the region of interest
	ROI_VERTICES = np.array([[(50, 540), (420, 330), (590, 330),(960 - 50, 540)]], dtype=np.int32)    

	# White and yellow color thresholds for lines masking.
	# Optional "kernel" key is used for additional morphology
	WHITE_LINES = { 'low_th': gimp_to_opencv_hsv(0, 0, 80),'high_th': gimp_to_opencv_hsv(359, 10, 100) }

	YELLOW_LINES = { 'low_th': gimp_to_opencv_hsv(35, 20, 30),'high_th': gimp_to_opencv_hsv(65, 100, 100),'kernel': np.ones((3,3),np.uint64)}

	def get_lane_lines_mask(hsv_image, colors):
    	#"""
    	#Image binarization using a list of colors. The result is a binary mask
    	#which is a sum of binary masks for each color.
    	#"""
    		masks = []
    		for color in colors:
        		if 'low_th' in color and 'high_th' in color:
            			mask = cv2.inRange(hsv_image, color['low_th'], color['high_th'])
            			if 'kernel' in color:
                			mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, color['kernel'])
            			masks.append(mask)
        		else: raise Exception('High or low threshold values missing')
    		if masks:
        		return cv2.add(*masks)
    
	def hough_line_transform(image, rho, theta, threshold, min_line_length, max_line_gap):
    	#"""
    	#A modified implementation of a suggested `hough_lines` function which allows 
    	#Line objects initialization and in-place line filtering.
    	#Returns a list of Line instances which are considered segments of a lane.
    	#"""
    		lines = cv2.HoughLinesP(image, rho, theta, threshold, np.array([]), minLineLength=min_line_length, maxLineGap=max_line_gap)
    		if lines is not None:
        		filtered_lines = list(filter(lambda l: l.candidate, map(lambda line: Line(*line[0]), lines)))
        		return filtered_lines
    		else: return None
    
	def update_lane(segments):
    		if segments is not None:
        		left = [segment for segment in segments if segment.lane_line == 'left_line']
        		right = [segment for segment in segments if segment.lane_line == 'right_line']
        		if not Lane.lines_exist():
            			Lane.left_line = Lane(left)
            			Lane.right_line = Lane(right)      
        	Lane.update_vanishing_point(Lane.left_line, Lane.right_line)
        	Lane.left_line.update_lane_line([l for l in left if l.candidate])
        	Lane.right_line.update_lane_line([r for r in right if r.candidate])

	def image_pipeline(image):
    	#"""
    	#Main image pipeline with 3 phases:
    	#* Raw image preprocessing and noise filtering;
    	#* Lane lines state update with the information gathered in preprocessing phase;
    	#* Drawing updated lane lines and other objects on image.
    	#"""

    	### Phase 1: Image Preprocessing

   		hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    		binary_mask = get_lane_lines_mask(hsv_image, [WHITE_LINES, YELLOW_LINES])

    		masked_image = draw_binary_mask(binary_mask, hsv_image)

    		blank_image = np.zeros_like(image)

    		edges_mask = canny(masked_image, 280, 360)
    
    		if not Lane.lines_exist():
        		edges_mask = region_of_interest(edges_mask, ROI_VERTICES)
    
    		edges_image = draw_canny_edges(edges_mask, blank_image)
    
    		segments = hough_line_transform(edges_mask, 1, math.pi / 180, 5, 5, 8)
    
    ### Stage 2: Lane lines state update
    
    		update_lane(segments)

    ### Stage 3: Drawing

    # Snapshot 1
    		out_snap1 = np.zeros_like(image)
    		out_snap1 = draw_binary_mask(binary_mask, out_snap1)
    		out_snap1 = draw_filtered_lines(segments, out_snap1)
    		snapshot1 = cv2.resize(deepcopy(out_snap1), (240,135))
    
    # Snapshot 2
    		out_snap2 = np.zeros_like(image)
    		out_snap2 = draw_canny_edges(edges_mask, out_snap2)
    		out_snap2 = draw_points(Lane.left_line.points, out_snap2, Lane.COLORS['left_line'])
    		out_snap2 = draw_points(Lane.right_line.points, out_snap2, Lane.COLORS['right_line'])
    		out_snap2 = draw_lane_polygon(out_snap2)
    		snapshot2 = cv2.resize(deepcopy(out_snap2), (240,135))
    
    # Augmented image
    		output = deepcopy(image)
    		output = draw_lane_lines([Lane.left_line, Lane.right_line], output, shade_background=True)
    		output = draw_dashboard(output, snapshot1, snapshot2)
    		return output

# Simple drawing routines to draw figures on image.

# Though cv2 functions mutate objects in arguments, 
# all routines below explicitly return a 3-channel RGB image.

# Basic signature: draw_some_object(what_to_draw, background_image_to_draw_on, kwargs)

	def draw_binary_mask(binary_mask, img):
    		if len(binary_mask.shape) != 2: 
        		raise Exception('binary_mask: not a 1-channel mask. Shape: {}'.format(str(binary_mask.shape)))
    		masked_image = np.zeros_like(img)
    		for i in range(3): 
        		masked_image[:,:,i] = binary_mask.copy()
    		return masked_image

	def draw_canny_edges(binary_mask, img):
    		return draw_binary_mask(binary_mask, img)

	def draw_filtered_lines(lines, img, color=[255, 0, 0], thickness=2):
    	#"""
    	#Uses the output of `hough_line_transform` function to draw lines on an image.
    	#"""
    		if lines is None: return img
    		line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    		for line in lines:
        		x1,y1,x2,y2 = line.get_coords()
        		cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    		return weighted_img(line_img, img)

	def draw_points(points, img, color=(255,255,0)):
    		if points is None: return img
    		for point in points:
        		cv2.circle(img, point, 2, color, -1)
    		return img

	def draw_lane_lines(lane_lines, img, shade_background=False):
    		if shade_background: a1 = 0.8
    		else: a1 = 1.
    		lane_line_image = np.zeros_like(img)
    		for line in lane_lines:
        		line.update_lane_line_coords()
        		cv2.line(lane_line_image, (line.x1, line.y1), (line.x2, line.y2),Lane.COLORS['lane_color'], Lane.THICKNESS)
    		return weighted_img(lane_line_image, img, a1=a1, b1=1.)
  
	def draw_lane_polygon(img):
    		offset_from_lane_edge = 20
    		color = Lane.COLORS['region_stable']
    
    		if not Lane.lines_exist(): return img

    # Polygon points
    		p1 = [Lane.left_line.x1,Lane.left_line.y1]
    		p2 = [Lane.left_line.get_x_coord(Lane.left_line.y2 + offset_from_lane_edge), Lane.left_line.y2 + offset_from_lane_edge]
    		p3 = [Lane.right_line.get_x_coord(Lane.left_line.y2 + offset_from_lane_edge),Lane.right_line.y2 + offset_from_lane_edge]
    		p4 = [Lane.right_line.x1,Lane.right_line.y1]
    
    		polygon_points = np.array([p1, p2, p3, p4], np.int32).reshape((-1,1,2))
    
    		if not Lane.left_line.stable or not Lane.right_line.stable:
        		color = Lane.COLORS['region_unstable']
    
    		poly_img = np.zeros_like(img)
    		cv2.fillPoly(poly_img,[polygon_points], color)
    		return weighted_img(img, poly_img)

	def draw_dashboard(img, snapshot1, snapshot2):
    # TODO: refactor this
    		if not Lane.lines_exist(): return img
    		cv2.CV_FILLED = -1
    		image_copy = deepcopy(img)
    		cv2.rectangle(image_copy, (0,0), (540,175), (0,0,0), cv2.CV_FILLED)
    		img = weighted_img(image_copy, img, a1=0.3, b1=0.7)
    		img[20:155,20:260,:] = snapshot1
    		img[20:155,280:520,:] = snapshot2
    		return img

	def draw_on_gray_with_color_mask(img, binary_mask):
    	#"""
    	#Returns a gray-ish image with colorized parts described in binary_mask.
    	#img should be a 3-channel image.
    	#"""
    		image_gray = grayscale(img)
    		mask = np.zeros_like(img)
    		color_mask = cv2.bitwise_and(img, img, mask= binary_mask)
    		binary_mask_inv = cv2.bitwise_not(binary_mask)
    		image_gray = cv2.bitwise_and(image_gray, image_gray, mask=binary_mask_inv)

    		output = np.zeros_like(img)
    		for i in range(3):
        		output[:,:,i] = image_gray
    		output = cv2.add(output, color_mask)
    		return output

	def grayscale(img):
    	#Applies the Grayscale transform
    	#This will return an image with only one color channel
    	#but NOTE: to see the returned image as grayscale
    	#(assuming your grayscaled image is called 'gray')
    	#you should call plt.imshow(gray, cmap='gray')
    		return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    	# Or use BGR2GRAY if you read an image with cv2.imread()
    	# return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
	def canny(img, low_threshold, high_threshold):
    	#Applies the Canny transform"""
    		return cv2.Canny(img, low_threshold, high_threshold)

	def gaussian_blur(img, kernel_size):
    	#Applies a Gaussian Noise kernel"""
    		return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

	def region_of_interest(img, vertices):
    	#"""
    	#Applies an image mask.
    
    	#Only keeps the region of the image defined by the polygon
    	#formed from `vertices`. The rest of the image is set to black.
    	#"""
    	#defining a blank mask to start with
    		mask = np.zeros_like(img)   
    
    	#defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    		if len(img.shape) > 2:
        		channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        		ignore_mask_color = (255,) * channel_count
    		else:
        		ignore_mask_color = 255
        
    	#filling pixels inside the polygon defined by "vertices" with the fill color    
    		cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    	#returning the image only where mask pixels are nonzero
    		masked_image = cv2.bitwise_and(img, mask)
    		return masked_image


	def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    	#"""
    	#NOTE: this is the function you might want to use as a starting point once you want to 
    	#average/extrapolate the line segments you detect to map out the full
    	#extent of the lane (going from the result shown in raw-lines-example.mp4
    	#to that shown in P1_example.mp4).  
    	
    	#Think about things like separating line segments by their 
    	#slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    	#line vs. the right line.  Then, you can average the position of each of 
    	#the lines and extrapolate to the top and bottom of the lane.
    	
    	#This function draws `lines` with `color` and `thickness`.    
    	#Lines are drawn on the image inplace (mutates the image).
    	#If you want to make the lines semi-transparent, think about combining
    	#this function with the weighted_img() function below
    	#"""
    		for line in lines:
        		for x1,y1,x2,y2 in line:
            			cv2.line(img, (x1, y1), (x2, y2), color, thickness)

	def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    	#"""
    	#`img` should be the output of a Canny transform.
    	#    
    	#Returns an image with hough lines drawn.
    	#"""
    		lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    		line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    		draw_lines(line_img, lines)
    		return line_img

# Python 3 has support for cool math symbols.

	def weighted_img(img, initial_img, a1=0.8, b1=1., c1=0.):
    	#"""
    	#`img` is the output of the hough_lines(), An image with lines drawn on it.
    	#Should be a blank image (all black) with lines drawn on it.
    	#
    	#`#initial_img` should be the image before any processing.
    	#
    	#The result image is computed as follows:
    	#
    	#	initial_img * 
    	#	NOTE: initial_img and img must be the same shape!
    	#"""
    		return cv2.addWeighted(initial_img, a1, img, b1, c1)