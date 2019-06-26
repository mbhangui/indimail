/*
 * $Log: dkimsign.h,v $
 * Revision 1.5  2019-06-26 19:09:07+05:30  Cprogrammer
 * added sOrigRecipient variable for X-Original-Recepient header added by qmail-send for bounces
 *
 * Revision 1.4  2017-09-05 10:59:20+05:30  Cprogrammer
 * removed compiler warnings
 *
 * Revision 1.3  2017-08-09 22:03:09+05:30  Cprogrammer
 * initialized EVP_MD_CTX variables
 *
 * Revision 1.2  2017-08-08 23:50:33+05:30  Cprogrammer
 * openssl 1.1.0 port
 *
 * Revision 1.1  2009-04-16 10:34:02+05:30  Cprogrammer
 * Initial revision
 *
 *
 *  Copyright 2005 Alt-N Technologies, Ltd. 
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); 
 *  you may not use this file except in compliance with the License. 
 *  You may obtain a copy of the License at 
 *
 *      http://www.apache.org/licenses/LICENSE-2.0 
 *
 *  This code incorporates intellectual property owned by Yahoo! and licensed 
 *  pursuant to the Yahoo! DomainKeys Patent License Agreement.
 *
 *  Unless required by applicable law or agreed to in writing, software 
 *  distributed under the License is distributed on an "AS IS" BASIS, 
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
 *  See the License for the specific language governing permissions and 
 *  limitations under the License.
 *
 */

#ifndef DKIMSIGN_H
#define DKIMSIGN_H

#include "dkimbase.h"

class           CDKIMSign:public CDKIMBase {
public:

	CDKIMSign();
	~CDKIMSign();
	int             Init(DKIMSignOptions * pOptions);
	int             GetSig(char *szPrivKey, char *szSignature, unsigned int nSigLength);
	int             GetSig2(char *szPrivKey, char **pszSignature);
	virtual int     ProcessHeaders(void);
	virtual int     ProcessBody(char *szBuffer, int nBufLength, bool bEOF);
	enum CKDKIMConstants { OptimalHeaderLineLength = 65 };
	char           *DKIM_CALL GetDomain(void);

protected:
	void            Hash(const char *szBuffer, int nBufLength, bool bHdr, bool bAllmanOnly = false);
	bool            SignThisTag(const string & sTag);
	void            GetHeaderParams(const string & sHdr);
	void            ProcessHeader(const string & sHdr);
	bool            ParseFromAddress(void);
	void            InitSig(void);
	void            AddTagToSig(char *Tag, const string & sValue, char cbrk, bool bFold);
	void            AddTagToSig(char *Tag, unsigned long nValue);
	void            AddInterTagSpace(int nSizeOfNextTag);
	void            AddFoldedValueToSig(const string & sValue, char cbrk);
	bool            IsRequiredHeader(const string & sTag);
	int             ConstructSignature(char *szPrivKey, bool bUseIetfBodyHash, bool bUseSha256);
	int             AssembleReturnedSig(char *szPrivKey);
#if OPENSSL_VERSION_NUMBER >= 0x10100000L
	EVP_MD_CTX     *m_Hdr_ietf_sha1ctx = NULL;	/* the header hash for ietf sha1  */
	EVP_MD_CTX     *m_Bdy_ietf_sha1ctx = NULL;	/* the body hash for ietf sha1  */
#ifdef HAVE_EVP_SHA256
	EVP_MD_CTX     *m_Hdr_ietf_sha256ctx = NULL;	/* the header hash for ietf sha256 */
	EVP_MD_CTX     *m_Bdy_ietf_sha256ctx = NULL;	/* the body hash for ietf sha256 */
#endif
	EVP_MD_CTX     *m_allman_sha1ctx = NULL;	/* the hash for allman sha1  */
#else
	EVP_MD_CTX      m_Hdr_ietf_sha1ctx;	/* the header hash for ietf sha1  */
	EVP_MD_CTX      m_Bdy_ietf_sha1ctx;	/* the body hash for ietf sha1  */
#ifdef HAVE_EVP_SHA256
	EVP_MD_CTX      m_Hdr_ietf_sha256ctx;	/* the header hash for ietf sha256 */
	EVP_MD_CTX      m_Bdy_ietf_sha256ctx;	/* the body hash for ietf sha256 */
#endif
	EVP_MD_CTX      m_allman_sha1ctx;	/* the hash for allman sha1  */
#endif
	int             m_Canon;	// canonization method
	int             m_EmptyLineCount;
	string          hParam;
	string          sFrom;
	string          sSender;
	string          sSelector;
	string          sReturnPath;
	string          sOrigRecipient; /*- used for bounces */
	string          sDomain;
	string          sIdentity;	// for i= tag, if empty tag will not be included in sig
	string          sRequiredHeaders;
	bool            m_IncludeBodyLengthTag;
	int             m_nBodyLength;
	time_t          m_ExpireTime;
	int             m_nIncludeTimeStamp;	// 0 = don't include t= tag, 1 = include t= tag
	int             m_nIncludeQueryMethod;	// 0 = don't include q= tag, 1 = include q= tag
	int             m_nHash;	// use one of the DKIM_HASH_xx constants here
	int             m_nIncludeCopiedHeaders;	// 0 = don't include z= tag, 1 = include z= tag
	int             m_nIncludeBodyHash;	// 0 = calculate sig using draft 0, 1 = include bh= tag and 
	// use new signature computation algorithm
	DKIMHEADERCALLBACK m_pfnHdrCallback;
	string          m_sSig;
	int             m_nSigPos;
	string          m_sReturnedSig;
	bool            m_bReturnedSigAssembled;
	string          m_sCopiedHeaders;
};

#endif	/*- DKIMSIGN_H */
