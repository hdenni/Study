#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <string.h>

class TW_String {
private:
	char m_string[24];
public:
	void SetString(const char* ap_string)
	{
		strcpy(m_string, ap_string);
	}
	char* operator+(const char* ap_string)
	{
		return strcat(m_string, ap_string);
	}
};

int main()
{
	TW_String str1;
	str1.SetString("abc");

	char* p_string = str1 + "def";
	printf("%s\n", p_string);
}
