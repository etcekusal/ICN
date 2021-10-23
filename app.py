import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Calculate Partitioning Layer Index(Single Edge Device) and Explore Variation in different parameters by Graphical Approach")
name = st.selectbox('Chose Network Architecture ',('VGG16', 'ResNet', 'MobileNetv1','None'))
dic={"VGG16":"vgg16","ResNet":"resnet","MobileNetv1":"mobilenetv1"}
if name!="None":
    file_name = "data_"+dic[name]+".xlsx"
    df = pd.read_excel(file_name)
    ratio = df.iloc[:,6]
    memory_output = df.iloc[:,15]
    cloud_inference_time_orig = df.iloc[:,7]
else:
    excel_file = st.file_uploader("Upload the CSV File")
    st.text("Note : Excel file should contain Approximate Ratio in calumn G , Cloud Inference time(ms) \nin calumn H , Memory consumed(Bytes) for output in calumn P")
    if excel_file != None:
        df = pd.read_excel(excel_file)
        ratio = df.iloc[:,6]
        memory_output = df.iloc[:,15]
        cloud_inference_time_orig = df.iloc[:,7]
st.subheader("==================================================")
st.subheader("\n")
st.text("Use the specified Zeroth Layer Input Memory for your chosed Network : \n VGG16 \t\t 12288 Bytes\n ResNet\t\t 14700 Bytes\n MobileNetv1\t 150528 Bytes\n\nOtherwise use your own network's Zeroth Layer Input memory ")
st.subheader("\n")
def calculate_total_inference_time(ratio,F,memory_output,B,input_memory,cloud_inference_time):
    rasp_pi_inference_time = []
    for i in range(len(ratio)):
        rasp_pi_inference_time.append(1000*ratio[i]/F)

    transmit_time = []
    for i in range(len(memory_output)):
        transmit_time.append(1000*memory_output[i]/(B*(2**17)))

    zeroth_layer_transmit_time=1000*input_memory/(B*(2**17))

    total_inference_time=[zeroth_layer_transmit_time+sum(cloud_inference_time)+transmit_time[-1]]
    for i in range(len(transmit_time)):
        temp=0
        for j in range(i+1):
            temp+=rasp_pi_inference_time[j]
        temp+=transmit_time[i]
        for j in range(i+1,len(transmit_time)):
            temp+=cloud_inference_time[j]
        temp+=transmit_time[-1]
        total_inference_time.append(temp)
    np_arr = np.array(total_inference_time)
    partitioning_layer = np.argmin(np_arr)
    optimum_inference_time = total_inference_time[partitioning_layer]
    return total_inference_time,partitioning_layer,optimum_inference_time

if __name__=="__main__":
    F = st.number_input("FPS of the device : ",step=1.,format="%.2f")
    B = st.number_input("Bandwidth(Mbps) : ",step=1.,format="%.2f")
    input_memory = st.number_input("Zeroth Layer Input memory(Bytes) : ",step=1,format="%i")
    slowness_factor_cloud = st.number_input("Slowness factor of cloud server : ",step=1.,format="%.2f")
    col1, col2, col3 , col4, col5 = st.columns(5)
    check = False
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        check = st.button("Submit")
    if check==True:
        cloud_inference_time = cloud_inference_time_orig*slowness_factor_cloud
        total_inference_time,p,o = calculate_total_inference_time(ratio,F,memory_output,B,input_memory,cloud_inference_time)
        st.success("Partitioning Layer Index is "+str(p)+" and optimum time is "+str(o)+" ms")
        st.line_chart(total_inference_time)
    st.title("FPS Variation ")
    F1 = st.number_input("FPS of the device(1) : ",step=1.,format="%.2f")
    F2 = st.number_input("FPS of the device(2) : ",step=1.,format="%.2f")
    F3 = st.number_input("FPS of the device(3) : ",step=1.,format="%.2f")
    B_fps = st.number_input("Bandwidth(Mbps) for FPS Variation Checking: ",step=1.,format="%.2f")
    input_memory_fps = st.number_input("Zeroth Layer Input memory(Bytes) for FPS Variation Checking: ",step=1,format="%i")
    slowness_factor_cloud_fps = st.number_input("Slowness factor of cloud server for FPS Variation Checking: ",step=1.,format="%.2f")
    col1, col2, col3 , col4, col5 = st.columns(5)
    check1 = False
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        check1 = st.button("Get FPS Variation")
    if check1==True:
        cloud_inference_time = cloud_inference_time_orig*slowness_factor_cloud_fps

        total_inference_time_1,p1,o1 = calculate_total_inference_time(ratio,F1,memory_output,B_fps,input_memory_fps,cloud_inference_time)
        total_inference_time_2,p2,o2 = calculate_total_inference_time(ratio,F2,memory_output,B_fps,input_memory_fps,cloud_inference_time)
        total_inference_time_3,p3,o3 = calculate_total_inference_time(ratio,F3,memory_output,B_fps,input_memory_fps,cloud_inference_time)
        fig,ax=plt.subplots(figsize=(12,5))
        ax.plot(total_inference_time_1)
        ax.plot(total_inference_time_2)
        ax.plot(total_inference_time_3)
        ax.legend([F1,F2,F3])
        ax.plot(p1,o1,'o')
        ax.plot(p2,o2,'o')
        ax.plot(p3,o3,'o')
        st.pyplot(fig)
        st.text("Device\t\tPartitioning Layer\t\tOptimum time\n"+"1\t\t\t"+str(p1)+"\t\t\t"+str(o1)+"\n2\t\t\t"+str(p2)+"\t\t\t"+str(o2)+"\n3\t\t\t"+str(p3)+"\t\t\t"+str(o3))

    st.title("Bandwidth Variation ")
    B1= st.number_input("Bandwidth(Mbps)(1): ",step=1.,format="%.2f")
    B2= st.number_input("Bandwidth(Mbps)(2): ",step=1.,format="%.2f")
    B3= st.number_input("Bandwidth(Mbps)(3): ",step=1.,format="%.2f")
    F_bw = st.number_input("FPS of the device for Bandwidth variation : ",step=1.,format="%.2f")
    input_memory_bw = st.number_input("Zeroth Layer Input memory(Bytes) for Bandwidth Variation Checking: ",step=1,format="%i")
    slowness_factor_cloud_bw = st.number_input("Slowness factor of cloud server for Bandwidth Variation Checking: ",step=1.,format="%.2f")
    col1, col2, col3 , col4, col5 = st.columns(5)
    check2 = False
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        check2 = st.button("Get Bandwidth Variation")
    if check2==True:
        cloud_inference_time = cloud_inference_time_orig*slowness_factor_cloud_bw

        total_inference_time_1,p1,o1 = calculate_total_inference_time(ratio,F_bw,memory_output,B1,input_memory_bw,cloud_inference_time)
        total_inference_time_2,p2,o2 = calculate_total_inference_time(ratio,F_bw,memory_output,B2,input_memory_bw,cloud_inference_time)
        total_inference_time_3,p3,o3 = calculate_total_inference_time(ratio,F_bw,memory_output,B3,input_memory_bw,cloud_inference_time)
        fig,ax=plt.subplots(figsize=(12,5))
        ax.plot(total_inference_time_1)
        ax.plot(total_inference_time_2)
        ax.plot(total_inference_time_3)
        ax.legend([B1,B2,B3])
        ax.plot(p1,o1,'o')
        ax.plot(p2,o2,'o')
        ax.plot(p3,o3,'o')
        st.pyplot(fig)
        st.text("Device\t\tPartitioning Layer\t\tOptimum time\n"+"1\t\t\t"+str(p1)+"\t\t\t"+str(o1)+"\n2\t\t\t"+str(p2)+"\t\t\t"+str(o2)+"\n3\t\t\t"+str(p3)+"\t\t\t"+str(o3))
    
    st.title("Slowness Factor Variation of Cloud Server")
    F_sf = st.number_input("FPS of the device for Slowness Factor variation : ",step=1.,format="%.2f")
    B_sf = st.number_input("Bandwidth(Mbps) for Slowness Factor Variation : ",step=1.,format="%.2f")
    input_memory_sf = st.number_input("Zeroth Layer Input memory(Bytes) for Slowness Factor Variation : ",step=1,format="%i")
    S1 = st.number_input("Slowness Factor(1) : ",step=1.,format="%.2f")
    S2 = st.number_input("Slowness Factor(2) : ",step=1.,format="%.2f")
    S3 = st.number_input("Slowness Factor(3) : ",step=1.,format="%.2f")
    col1, col2, col3 , col4, col5 = st.columns(5)
    check3 = False
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        check3 = st.button("Get Slowness Factor Variation")
    if check3==True:
        cloud_inference_time_1 = cloud_inference_time_orig*S1
        cloud_inference_time_2 = cloud_inference_time_orig*S2
        cloud_inference_time_3 = cloud_inference_time_orig*S3

        total_inference_time_1,p1,o1 = calculate_total_inference_time(ratio,F_sf,memory_output,B_sf,input_memory_sf,cloud_inference_time_1)
        total_inference_time_2,p2,o2 = calculate_total_inference_time(ratio,F_sf,memory_output,B_sf,input_memory_sf,cloud_inference_time_2)
        total_inference_time_3,p3,o3 = calculate_total_inference_time(ratio,F_sf,memory_output,B_sf,input_memory_sf,cloud_inference_time_3)
        fig,ax=plt.subplots(figsize=(12,5))
        ax.plot(total_inference_time_1)
        ax.plot(total_inference_time_2)
        ax.plot(total_inference_time_3)
        ax.legend([S1,S2,S3])
        ax.plot(p1,o1,'o')
        ax.plot(p2,o2,'o')
        ax.plot(p3,o3,'o')
        st.pyplot(fig)
        st.text("Device\t\tPartitioning Layer\t\tOptimum time\n"+"1\t\t\t"+str(p1)+"\t\t\t"+str(o1)+"\n2\t\t\t"+str(p2)+"\t\t\t"+str(o2)+"\n3\t\t\t"+str(p3)+"\t\t\t"+str(o3))
    st.subheader("By Kusal Bhattacharyya , UG Student from Department Of ETCE , JU")
