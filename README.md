<div  align="center">
<h1><b>BKAR - Xe tự lái cấp độ 2</b></h1>
<p><b>Xe tự lái với máy tính nhúng AI NVIDIA Jetson Nano</b></p>

![Cover Photo](images/bkar.jpg)
</div>

<br>
<h2><b>1. Cấu tạo</b></h2>
<h3><b>1.1. Phần cứng</b></h3>
<ul>
<li>NVIDIA Jetson Nano B01 4GB RAM, Intel 8265NGW card, Vỏ Mica và quạt tản nhiệt pwm</li>
<li>MicroSD Card 64GB Class 10</li>
<li><a href="https://www.waveshare.com/imx219-83-stereo-camera.htm">Waveshare IMX219-83 Stereo Camera</a> gắn phía trước.</li>
<li>3 Camera hai bên và phía sau</li>
<li>Motor Driver L298N</li>
<li>MPU6050 GY-521 Acceleration Gyroscope Module</li>
<li>Lithium Baterry 12V DC</li>
<li>DC-DC 24/12V to 5V-4A Converter</li>
<li>Khung mica, động cơ</li>
<li>Tay điều khiển Joystick Xbox</li>
<li>Ốc vít, dây kết nối, đèn led, v.v.</li>
</ul>
<h3><b>1.2. Phần mềm</b></h3>
<ul>
<li>Object detection</li>
<li>Lane detection</li>
<li>Traffic Light detection</li>
<li>Traffic Signs detection</li>
<li>Parking Spot detection</li>
<li>NVIDIA DeepStream</li>
<li>TensorFlow</li>
<li>TensorRT</li>
<li>NVIDIA Docker</li>
</ul>

<br>
<h2><b>2. Các chức năng chính</b></h2>
<ul>
<li>Camera 360.</li>
<li>Nhận dạng biển báo, nơi đỗ xe, ngã ba, ngã tư, khúc cua, vạch kẻ đường.</li>
<li>Tự động rẽ</li>
<li>Tự động giữ làn</li>
<li>Tự động ra vào nơi đỗ xe(ghép chuồng ngang, dọc).</li>
<li>Tự động lái tới vị trí chỉ định trên bản đồ.</li>
</ul>

<br>
<h2><b>3. Bản đồ</b></h2>
<h3><b>3.1 Giai đoạn 1</b></h3>
Bản đồ đơn giản với hai làn đường song song, không có nhánh rẽ, chỉ có 4 khúc cua. Nhằm phát triển các tính năng giữ làn, chuyển làn. Ngoài ra giúp kiểm tra tính ổn định của các thành phần khác của hệ thống như hệ thống stream video, điều khiển từ xa, các cảm biến, v.v.
<div align="center">
    <image src="./images/Map2.jpg">
</div>
<h3><b>3.2 Giai đoạn 2</b></h3>
Bản đồ phức tạp hơn với các ngã 3, ngã tư, đường quanh co, biển báo giao thông, đèn tín hiệu giao thông, v.v. Giúp phát triển các tính năng tự hành, tuân thủ vạch kẻ đường, biển báo, v.v. Ngoài ra có các chuồng đỗ xe dọc và ngang, phát triển tính năng lùi vào bãi đỗ, triệu hồi xe.
<div align="center">
    <image src="./images/Map.jpg">
</div>

<br>
<h2><b>4. Trạm sạc</b></h2>
<div align="center">
    <image src="./images/ChargingStation.jpg">
</div>
