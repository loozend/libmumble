# Copyright (c) 2013 The libmumble Developers
# The use of this source code is goverened by a BSD-style
# license that can be found in the LICENSE-file.

{
	'targets': [
		{
			'target_name':  'libmumble',
			'product_name': 'mumble',
			'type':         'static_library',
			'cflags_cc':    ['-std=c++11'],
			'dependencies': [
				'3rdparty/libuvbuild/uv.gyp:libuv',
				'3rdparty/opensslbuild/OpenSSL.gyp:libcrypto',
				'3rdparty/opensslbuild/OpenSSL.gyp:libssl',
				'3rdparty/protobufbuild/protobuf.gyp:protobuf_lite',
			],
			'include_dirs': [
				'include',
				'src',
				'3rdparty/libuv/include',
				'3rdparty/opensslbuild/include',
			],
			'sources': [
				'src/TLSConnection.cpp',
				'src/TLSConnection_p.cpp',
				'src/UVBio.cpp',
				'src/ByteArray.cpp',
				'src/X509Certificate.cpp',
				'src/X509Certificate_p.cpp',
				'src/X509PEMVerifier.cpp',
				'src/X509Verifier_unix.cpp',
				'src/X509HostnameVerifier.cpp',
				'src/OpenSSLUtils.cpp',
				'src/UVUtils.cpp',
				'src/Error.cpp',
				'src/Utils.cpp',
			],
			'conditions': [
				['use_system_protobuf==0', {
					'sources': [
						'proto/Mumble.pb.cpp',
						'proto/Mumble.pb.h',
					],
				},{
					'sources': [
						'proto/Mumble.proto',
					],
					'includes': [
						'3rdparty/protobufbuild/protoc.gypi',
					],
				}],
				['OS=="linux"', {
					'defines': ['LIBMUMBLE_OS_LINUX'],
					'link_settings': {
						'libraries': [ '-lpthread', '-lrt' ],
					},
				}],
				['OS=="mac"', {
					'defines': ['LIBMUMBLE_OS_MAC'],
					'xcode_settings': {
						'CLANG_CXX_LANGUAGE_STANDARD': 'c++0x',
						'CLANG_CXX_LIBRARY': 'libc++',
					},
					'link_settings': {
						'libraries': [
							'$(SDKROOT)/System/Library/Frameworks/Foundation.framework',
							'$(SDKROOT)/System/Library/Frameworks/Security.framework',
							'$(SDKROOT)/System/Library/Frameworks/CoreFoundation.framework',
						],
					},
					'sources!': [
						'src/X509Verifier_unix.cpp',
					],
					'sources': [
						'src/X509Verifier_mac.mm',
					],
				}],
				['OS=="ios"', {
					'defines': ['LIBMUMBLE_OS_IOS'],
					'xcode_settings': {
						'CLANG_CXX_LANGUAGE_STANDARD': 'c++0x',
						'CLANG_CXX_LIBRARY': 'libc++',
					},
					'link_settings': {
						'libraries': [
							'$(SDKROOT)/System/Library/Frameworks/Foundation.framework',
							'$(SDKROOT)/System/Library/Frameworks/Security.framework',
							'$(SDKROOT)/System/Library/Frameworks/CoreFoundation.framework',
						],
					},
					'sources!': [
						'src/X509Verifier_unix.cpp',
					],
					'sources': [
						'src/X509Verifier_mac.mm',
					],
				}],
				['OS=="win"', {
					'defines': [ 'LIBMUMBLE_OS_WINDOWS' ],
					'link_settings': {
						'libraries': [
							'crypt32',
						],
					},
					'sources!': [
						'src/X509Verifier_unix.cpp',
					],
					'sources': [
						'src/Compat_win.cpp',
						'src/X509Verifier_win.cpp',
					],
				}],
				['OS=="android"', {
					'defines': [ 'LIBMUMBLE_OS_ANDROID', '__STDC_LIMIT_MACROS' ],
					'sources!': [
						'src/X509Verifier_unix.cpp',
					],
					'sources': [
						'src/Compat_android.cpp',
						'src/X509Verifier_android.cpp',
					],
				}],
			],
		},
		{
			'target_name':   'libmumble-test',
			'product_name':  'libmumble-test',
			'type':          'executable',
			'cflags_cc':     ['-std=c++11'],
			'dependencies':  [
				'libmumble',
			],
			'include_dirs': [
				'include',
				'src',
				'3rdparty/libuv/include',
				'3rdparty/opensslbuild/include',
				'3rdparty/gtest/include',
				'3rdparty/gtest',
			],
			'sources': [
				'src/ByteArray_test.cpp',
				'src/mumble_test.cpp',
				'src/X509Certificate_test.cpp',
				'src/X509HostnameVerifier_test.cpp',
				'src/X509Verifier_test.cpp',
			],
			'conditions': [
				['OS=="mac"', {
					'xcode_settings': {
						'CLANG_CXX_LANGUAGE_STANDARD': 'c++0x',
						'CLANG_CXX_LIBRARY': 'libc++',
					},
					'defines': [
						'GTEST_HAS_TR1_TUPLE=0',
						'GTEST_USE_OWN_TR1_TUPLE=1',
					],
				}],
				['OS=="ios"', {
					'product_extension': 'app',
					'mac_bundle': 1,
					'xcode_settings': {
						'CLANG_CXX_LANGUAGE_STANDARD': 'c++0x',
						'CLANG_CXX_LIBRARY': 'libc++',
						'OTHER_CFLAGS': [
							'-fobjc-abi-version=2', # required for iphonesimulator to work as expected.
						],
						'INFOPLIST_FILE': 'build/iphoneos/test-bundle/Info.plist',
					},
					'mac_bundle_resources': [
						'<!@(find testdata -type f)',
					],
					'defines': [
						'LIBMUMBLE_OS_IOS=1',
						'GTEST_HAS_TR1_TUPLE=0',
						'GTEST_USE_OWN_TR1_TUPLE=1',
					],
					'include_dirs': [
						'3rdparty/gtestbuild/ios/include',
					],
					'sources': [
						'src/mumble_test.mm',
						'3rdparty/gtestbuild/ios/crt_externs.c',
					],
					'sources!': [
						'src/mumble_test.cpp',
					],
				}],
				['OS=="win"', {
					'defines': [
						'GTEST_HAS_TR1_TUPLE=0',
						'GTEST_USE_OWN_TR1_TUPLE=1',
					],
					'sources': [
						'src/Compat_win_test.cpp',
					],
				}],
				['OS=="android"', {
					'defines': ['__STDC_LIMIT_MACROS' ],
					'sources': [
						'src/Compat_android_test.cpp',
					],
				}],
			],
		},
		{
			'target_name':   'libmumble-demo',
			'product_name':  'libmumble-demo',
			'type':          'executable',
			'cflags_cc':     ['-std=c++11'],
			'dependencies':  [
				'libmumble',
			],
			'include_dirs': [
				'include',
				'src',
				'3rdparty/libuv/include',
				'3rdparty/opensslbuild/include',
				'3rdparty/gtest/include',
				'3rdparty/gtest',
			],
			'sources': [
				'src/demo.cpp',
			],
			'conditions': [
				['OS=="mac"', {
					'xcode_settings': {
						'CLANG_CXX_LANGUAGE_STANDARD': 'c++0x',
						'CLANG_CXX_LIBRARY': 'libc++',
					},
				}],
				['OS=="ios"', {
					'product_extension': 'app',
					'mac_bundle': 1,
					'xcode_settings': {
						'CLANG_CXX_LANGUAGE_STANDARD': 'c++0x',
						'CLANG_CXX_LIBRARY': 'libc++',
						'OTHER_CFLAGS': [
							'-fobjc-abi-version=2', # required for iphonesimulator to work as expected.
						],
						'INFOPLIST_FILE': 'build/iphoneos/demo-bundle/Info.plist',
					},
				}],
				['OS=="android"', {
					'defines': ['__STDC_LIMIT_MACROS' ],
				}],
			],
		},
	],
}
