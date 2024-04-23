## rapidjson
[介绍](https://blog.csdn.net/fengbingchun/article/details/91139889)
[源码](https://github.com/Tencent/rapidjson) 
c++使用rapidjson工具进行json文件格式化输出
```c++
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"

int main(){
    string video_path = "xxx.mp4";
    StringBuffer buf;
    Writer<StringBuffer> writer(buf);
    writer.StartObject();
    writer.Key("filename");
    writer.String(video_path.c_str());
    writer.Key("result");
    writer.StartArray();
    writer.Int(15);
    writer.EndArray();
    writer.EndObject();
    const char* json_content = buf.GetString();
    std::ofstream outfile(outFile);
    outfile << json_content << endl;
}

```